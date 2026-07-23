import telebot
import schedule
import time
import threading
import json
import random
import os
from datetime import datetime

# ========== بياناتك هنا ==========
TOKEN = os.environ.get("TOKEN", "ضع_التوكن_هنا")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "@معرف_قناتك")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "123456789"))
# =================================

bot = telebot.TeleBot(TOKEN)

try:
    with open('posts.json', 'r', encoding='utf-8') as f:
        posts_data = json.load(f)
except:
    posts_data = [
        "سبحان الله وبحمده، سبحان الله العظيم",
        "اللهم صلِّ وسلم وبارك على سيدنا محمد",
        "استغفر الله العظيم وأتوب إليه",
        "لا حول ولا قوة إلا بالله",
        "اللهم إني أسألك علماً نافعاً ورزقاً طيباً وعملاً متقبلاً"
    ]
    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts_data, f, ensure_ascii=False, indent=2)

used_posts = []

def save_posts():
    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts_data, f, ensure_ascii=False, indent=2)

def get_random_post():
    global used_posts
    available = [p for p in posts_data if p not in used_posts]
    if not available:
        used_posts = []
        available = posts_data
    post = random.choice(available)
    used_posts.append(post)
    return post

def send_to_channel():
    try:
        message = get_random_post()
        bot.send_message(CHANNEL_ID, message)
        print(f"تم النشر: {message[:50]}...")
    except Exception as e:
        print(f"خطأ: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id != ADMIN_ID:
        return
    from telebot import types
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add('📝 إضافة منشور', '📋 عرض المنشورات', '⏰ تغيير الجدولة', '📊 حالة البوت', '🔔 نشر فوري')
    bot.send_message(message.chat.id, "⚙️ لوحة تحكم البوت", reply_markup=markup)

@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID)
def admin_panel(msg):
    from telebot import types
    if msg.text == '📝 إضافة منشور':
        sent = bot.send_message(msg.chat.id, "أرسل المنشور الجديد:")
        bot.register_next_step_handler(sent, save_new_post)
    elif msg.text == '📋 عرض المنشورات':
        text = "\n".join(f"{i+1}. {p[:70]}" for i, p in enumerate(posts_data[:10]))
        bot.send_message(msg.chat.id, f"📚 {len(posts_data)} منشور:\n{text}")
    elif msg.text == '⏰ تغيير الجدولة':
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(*[types.InlineKeyboardButton(f"كل {h} س", callback_data=f"sch_{h}") for h in [1,2,4,6,12]])
        markup.add(types.InlineKeyboardButton("⏰ وقت يومي", callback_data="sch_custom"))
        bot.send_message(msg.chat.id, "اختر التوقيت:", reply_markup=markup)
    elif msg.text == '📊 حالة البوت':
        bot.send_message(msg.chat.id, f"📝 المنشورات: {len(posts_data)}")
    elif msg.text == '🔔 نشر فوري':
        send_to_channel()
        bot.send_message(msg.chat.id, "✅ تم النشر")

def save_new_post(message):
    posts_data.append(message.text)
    save_posts()
    bot.send_message(message.chat.id, f"✅ تمت الإضافة، العدد: {len(posts_data)}")

@bot.callback_query_handler(func=lambda c: c.data.startswith('sch_'))
def set_schedule(call):
    schedule.clear()
    val = call.data.split('_')[1]
    if val == 'custom':
        sent = bot.send_message(call.message.chat.id, "أرسل الوقت (مثال 14:30):")
        bot.register_next_step_handler(sent, set_custom_time)
        return
    schedule.every(int(val)).hours.do(send_to_channel)
    bot.send_message(call.message.chat.id, f"✅ كل {val} ساعة")

def set_custom_time(message):
    try:
        h, m = map(int, message.text.split(':'))
        schedule.every().day.at(f"{h:02d}:{m:02d}").do(send_to_channel)
        bot.send_message(message.chat.id, f"✅ يومياً {h:02d}:{m:02d}")
    except:
        bot.send_message(message.chat.id, "❌ خطأ بالصيغة")

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    schedule.every(2).hours.do(send_to_channel)
    threading.Thread(target=run_scheduler, daemon=True).start()
    print("✅ البوت يعمل...")
    bot.polling(none_stop=True)
