from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_RU
from database.database import user_db


def create_weather_settings_kb(user_id: int) -> ReplyKeyboardMarkup:
    id_text = ''

    kb_builder = ReplyKeyboardBuilder()
    locations = KeyboardButton(
        text='Точки интереса'
    )

    if user_db[user_id]['flag_daily_forecast']:
        id_text = 'Включено'
    else:
        id_text = 'Отключено'
    daily_forecast = KeyboardButton(
        text='Прогноз на день: ' + id_text
    )
    if user_db[user_id]['flag_weekly_forecast']:
        id_text = 'Включено'
    else:
        id_text = 'Отключено'
    weekly_forecast = KeyboardButton(
        text='Прогноз на неделю: ' + id_text
    )
    default_location = KeyboardButton(
        text='Дефолтное место: ' + user_db[user_id]['default_location']
    )

    # if user_db[user_id]['flag_default_location']:
    #     id_text = 'Геопозиция'
    # else:
    #     id_text = 'Место'
    # flag_default_location = KeyboardButton(
    #     text='Дефолтное место или геопозиция: ' + id_text
    # )
    close = KeyboardButton(
        text='Вернуться на главный экран'
    )
    kb_builder.row(locations, daily_forecast, weekly_forecast,
                   default_location, close, width=1)

    keyboard: ReplyKeyboardMarkup = kb_builder.as_markup()
    return keyboard


def create_location_kb(args) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for button in args:
        kb_builder.row(
            InlineKeyboardButton(
                text=f'''{button}: ({str(args[button][0])}, {
                    str(args[button][1])})''',
                callback_data=f'del_location {button}'
            )
        )

    keyboard: InlineKeyboardMarkup = kb_builder.as_markup(resize_keyboard=True)
    return keyboard


def create_choose_default_location_kb(args) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for button in args:
        kb_builder.row(
            InlineKeyboardButton(
                text=f'''{button}: ({str(args[button][0])}, {
                    str(args[button][1])})''',
                callback_data=f'def_location {button}'
            )
        )

    keyboard: InlineKeyboardMarkup = kb_builder.as_markup(resize_keyboard=True)
    return keyboard


def choose_locations_kb() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    add_locations = KeyboardButton(
        text='Добавить'
    )
    del_daily_forecast = KeyboardButton(
        text='Удалить'
    )
    cancel = KeyboardButton(
        text='Отмена'
    )
    look = KeyboardButton(
        text='Посмотреть'
    )
    kb_builder.row(add_locations, del_daily_forecast, look, cancel)

    keyboard: ReplyKeyboardMarkup = kb_builder.as_markup()
    return keyboard


def cancel_kb() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    cancel = KeyboardButton(
        text='Отмена'
    )
    kb_builder.row(cancel)
    keyboard: ReplyKeyboardMarkup = kb_builder.as_markup()
    return keyboard


def create_choose_forecast_kb() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    weather_now = InlineKeyboardButton(
        text='Погода сейчас',
        callback_data='weather_now',
    )
    daily_forecast = InlineKeyboardButton(
        text='Прогноз на день',
        callback_data='daily_forecast',
    )
    weekly_forecast = InlineKeyboardButton(
        text='Прогноз на неделю',
        callback_data='weekly_forecast',
    )
    kb_builder.row(weather_now, daily_forecast, weekly_forecast)
    keyboard: InlineKeyboardMarkup = kb_builder.as_markup(resize_keyboard=True)
    return keyboard
