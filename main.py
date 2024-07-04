from aiogram import Dispatcher, Bot
from config_data.config import Config, load_config
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
from aiogram import BaseMiddleware
from handlers import other_handlers, user_handlers, weather_settings_handlers
from keyboards.main_menu import set_main_menu
from aiogram.fsm.storage.memory import MemoryStorage
from database.db_module import db


class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler):
        super().__init__()
        self._scheduler = scheduler

    async def __call__(self, handler, event, data):
        # прокидываем в словарь состояния scheduler
        data["scheduler"] = self._scheduler
        return await handler(event, data)


async def my_scheduler(bot: Bot, scheduler: AsyncIOScheduler):
    scheduler.add_job(weather_settings_handlers.daily_forecast, 'cron', hour=7,
                      minute=0, args=(bot,))
    # задаём выполнение задачи по cron - гибкий способ задавать расписание.
    scheduler.add_job(weather_settings_handlers.weekly_forecast, 'cron', hour=7,
                      minute=0, args=(bot,))


async def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logging.info('Starting bot')
    scheduler = AsyncIOScheduler(timezone='Asia/Yekaterinburg')
    scheduler.start()

    storage = MemoryStorage()

    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token)

    await my_scheduler(bot, scheduler)

    dp = Dispatcher(storage=storage)
    dp.update.middleware(
        SchedulerMiddleware(scheduler=scheduler),
    )
    dp.startup.register(set_main_menu)

    dp.include_router(weather_settings_handlers.router)
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
