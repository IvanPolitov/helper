from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon_ru import LEXICON_COMMANDS
from aiogram.filters import Command, CommandStart, StateFilter
from keyboards.weather_kb import create_weather_settings_kb, create_choose_forecast_kb
from keyboards.main_window import create_main_window_kb
from services.weather import WeatherOpenMeteo
from services.geocoding import Geocoding
from states.states import FSMWeather
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from database.db_module import db
import logging

router = Router()
weather = WeatherOpenMeteo()
geocod = Geocoding()


# Команда хэлп выдаёт сообщение о возможностях бота и информацию о командах
@router.message(Command(commands='help'))
async def call_help(message: Message):
    await message.answer(text=LEXICON_COMMANDS['/help'])


# Команда старт добавляет пользователя в базу данных или (если он уже здесь)
# говорит доброе утро. Ну и создает главный экран
@router.message(CommandStart())
async def call_start(message: Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    if not user:
        db.create_user(message.from_user.id)
        logging.info(f'Пользователь добавлен {message.from_user.id}')
        # user_db[message.from_user.id] = deepcopy(user_dict_template)
        await message.answer(text=f'Добро пожаловать, {message.from_user.first_name}. Новый пользователь добавлен. {LEXICON_COMMANDS['/start']}', reply_markup=create_main_window_kb(message.from_user.id))
    else:
        await message.answer(text=f'Добрый день, {message.from_user.first_name}.', reply_markup=create_main_window_kb(message.from_user.id))
    await state.set_state(state=default_state)


# В меню расположена команда weather_settings.
# При нажатии мы переходим в состояние weather_settings_state
# и можем менять настройки бота
@router.message(Command(commands='weather_settings'))
async def change_weather_settings(message: Message, state: FSMContext):
    text = 'Настройки ваших прогнозов'
    await message.answer(text=text,
                         reply_markup=create_weather_settings_kb(message.from_user.id))
    await state.set_state(state=FSMWeather.weather_settings_state)


# Прогрузка главного экрана
@router.message(StateFilter(default_state), F.text == 'Главный экран')
async def main_window(message: Message):
    await message.answer(text='Главный экран', reply_markup=create_main_window_kb(message.from_user.id))


# Взаимодействие с меню прогнозов на ГЭ
@router.message(StateFilter(default_state), F.text == 'Погода')
async def get_weather(message: Message):
    await message.answer(text='Погода', reply_markup=create_choose_forecast_kb())


# Возвращаемся на главный экран с экрана погодных настроек
@router.message(StateFilter(FSMWeather.weather_settings_state))
async def return_main_window(message: Message, state: FSMContext):
    await call_start(message, state)


# Отмена для "выбора дефолтного места"
@ router.message(StateFilter(FSMWeather.choose_default_locations_state), F.text == 'Вернуться на главный экран')
async def return_main_window2(message: Message, state: FSMContext):
    await call_start(message, state)


# Запрос погоды в настоящее время в дефолтном месте
@router.callback_query(F.data == 'weather_now')
async def get_weather_now(callback: CallbackQuery):
    db_location = db.get_user_default_location(callback.from_user.id)
    # location = user_db[callback.from_user.id]['default_location']
    try:
        qq = weather.get_current_weather(
            # сюда пихается широта и долгота, распаковываем кортеж, который берем из словаря (до перехода в бд)
            # *user_db[callback.from_user.id]['locations'][location])
            *db_location[2:4])

        await callback.message.edit_text(
            text=qq,
            reply_markup=callback.message.reply_markup
        )
        await callback.answer()
    except KeyError:
        await callback.message.edit_text(
            text='Смените дефолтное место',
            reply_markup=callback.message.reply_markup
        )
        await callback.answer()


# Запрос прогноза на день в дефолтном месте
@router.callback_query(F.data == 'daily_forecast')
async def get_weather_daily(callback: CallbackQuery):
    db_location = db.get_user_default_location(callback.from_user.id)
    # location = user_db[callback.from_user.id]['default_location']
    try:
        qq = weather.get_daily_forecast(
            # *user_db[callback.from_user.id]['locations'][location])
            *db_location[2:4])

        await callback.message.edit_text(
            text=qq,
            reply_markup=callback.message.reply_markup
        )
        await callback.answer()
    except KeyError:
        await callback.message.edit_text(
            text='Смените дефолтное место',
            reply_markup=callback.message.reply_markup
        )
        await callback.answer()


# Запрос прогноза на неделю в дефолтном месте
@router.callback_query(F.data == 'weekly_forecast')
async def get_weather_weekly(callback: CallbackQuery):
    db_location = db.get_user_default_location(callback.from_user.id)
    # location = user_db[callback.from_user.id]['default_location']
    try:
        qq = weather.get_weekly_forecast(
            # *user_db[callback.from_user.id]['locations'][location])
            *db_location[2:4])

        await callback.message.edit_text(
            text=qq,
            reply_markup=callback.message.reply_markup
        )
        await callback.answer()
    except KeyError:
        await callback.message.edit_text(
            text='Смените дефолтное место',
            reply_markup=callback.message.reply_markup
        )
        await callback.answer()
