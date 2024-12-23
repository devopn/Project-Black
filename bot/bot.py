from aiogram import Bot, Dispatcher, types
import asyncio
from config import config
from handlers import handlers

async def main():
    bot = Bot(token=config.telegram.token)
    dp = Dispatcher()
    dp.include_routers(*handlers)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())