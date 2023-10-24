import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_reader import config
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import see_all_handler, see_types_handler, see_regions_handler

logging.basicConfig(level=logging.INFO)


# Запуск бота
async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(see_all_handler.router, see_types_handler.router, see_regions_handler.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
