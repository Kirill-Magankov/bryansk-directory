import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_reader import config
from aiogram import types
from aiogram.filters import Command
from handlers import start_handler

logging.basicConfig(level=logging.INFO)

# Запуск бота
async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_router(start_handler.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
