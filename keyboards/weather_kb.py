from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_RU
from database.db_module import db


def create_weather_settings_kb(user_id: int) -> ReplyKeyboardMarkup:
    id_text = ''
    user_flag_daily_forecast, user_flag_weekly_forecast, user_default_location = db.get_user(
        user_id)[1:]

    kb_builder = ReplyKeyboardBuilder()
    locations = KeyboardButton(
        text='Точки интереса'
    )

    if user_flag_daily_forecast:
        id_text = 'Включено'
    else:
        id_text = 'Отключено'
    daily_forecast = KeyboardButton(
        text='Прогноз на день: ' + id_text
    )
    if user_flag_weekly_forecast:
        id_text = 'Включено'
    else:
        id_text = 'Отключено'
    weekly_forecast = KeyboardButton(
        text='Прогноз на неделю: ' + id_text
    )
    default_location = KeyboardButton(
        text='Дефолтное место: ' + str(user_default_location)
    )

    close = KeyboardButton(
        text='Вернуться на главный экран'
    )
    kb_builder.row(locations, daily_forecast, weekly_forecast,
                   default_location, close, width=1)

    keyboard: ReplyKeyboardMarkup = kb_builder.as_markup()
    return keyboard


def create_location_kb(args) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for user_location in args:
        kb_builder.row(
            InlineKeyboardButton(
                text=f'''{user_location[-1]}: ({str(user_location[-3])}, {
                    str(user_location[-2])})''',
                callback_data=f'del_location {user_location[-1]}'
            )
        )

    keyboard: InlineKeyboardMarkup = kb_builder.as_markup(resize_keyboard=True)
    return keyboard


def create_choose_default_location_kb(args) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for user_location in args:
        kb_builder.row(
            InlineKeyboardButton(
                text=f'''{user_location[-1]}: ({str(user_location[-3])}, {
                    str(user_location[-2])}''',
                callback_data=f'def_location {user_location[-1]}'
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
