from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot

from config import BOT_TOKEN, CHANNEL_ID
from database import Database

db = Database()
scheduler = AsyncIOScheduler()


async def send_next_post():

    posts = db.get_posts()

    if len(posts) == 0:
        return

    current = db.get_current_post()

    if current >= len(posts):
        current = 0

    post = posts[current]

    bot = Bot(BOT_TOKEN)

    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=post[1]
    )

    current += 1

    if current >= len(posts):
        current = 0

    db.set_current_post(current)


def start_scheduler():

    scheduler.remove_all_jobs()

    hours = db.get_interval()

    scheduler.add_job(
        send_next_post,
        trigger="interval",
        hours=hours
    )

    if not scheduler.running:
        scheduler.start()


def stop_scheduler():

    scheduler.remove_all_jobs()


def restart_scheduler():

    stop_scheduler()

    start_scheduler()
