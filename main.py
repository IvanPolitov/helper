from aiogram.types import Message
from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command, CommandStart
from config_data.config import Config, load_config
import asyncio
from handlers import other_handlers


async def main() -> None:
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token)

    dp = Dispatcher()
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
