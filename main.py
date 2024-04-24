from aiogram import Dispatcher, Bot
from config_data.config import Config, load_config
import asyncio
import logging
from handlers import other_handlers, user_handlers
from keyboards.main_menu import set_main_menu
from aiogram.fsm.storage.memory import MemoryStorage


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logging.info('Starting bot')

    storage = MemoryStorage()

    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token)

    dp = Dispatcher(storage=storage)

    dp.startup.register(set_main_menu)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
