from aiogram import Dispatcher, Bot
from config_data.config import Config, load_config
import asyncio
from handlers import other_handlers, user_handlers
from keyboards.main_menu import set_main_menu


async def main() -> None:
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token)

    dp = Dispatcher()
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    # надо чекнуть как менять клавиатуру
    await bot.delete_my_commands()
    await set_main_menu(bot)

asyncio.run(main())
