import asyncio
import logging

from maxapi import Bot, Dispatcher

import config
from db.database import init_db
from handlers import register_handlers

logging.basicConfig(level=logging.INFO)

bot = Bot(config.MAX_BOT_TOKEN)
dp = Dispatcher()

register_handlers(dp)


async def main():
    init_db()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
