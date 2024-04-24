from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_RU


def create_weather_settings_kb() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    locations = KeyboardButton(
        text='Точки интереса'
    )
    daily_forecast = KeyboardButton(
        text='Прогноз на день'
    )
    weekly_forecast = KeyboardButton(
        text='Прогноз на неделю'
    )
    default_location = KeyboardButton(
        text='Дефолтное место'
    )
    flag_default_location = KeyboardButton(
        text='Дефолтное место или геопозиция'
    )
    close = KeyboardButton(
        text='Вернуться на главный экран'
    )
    kb_builder.row(locations, daily_forecast, weekly_forecast,
                   default_location, flag_default_location, close, width=1)

    keyboard: ReplyKeyboardMarkup = kb_builder.as_markup()
    return keyboard


def create_location_kb(args) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for button in args:
        kb_builder.row(
            InlineKeyboardButton(
                text=f'''{button}: ({str(args[button][0])}, {
                    str(args[button][1])})''',
                callback_data=f'del_location {str(args[button][0])} {
                    str(args[button][1])}'
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
    kb_builder.row(add_locations, del_daily_forecast, width=2)

    keyboard: ReplyKeyboardMarkup = kb_builder.as_markup()
    return keyboard


def cancel_locations_kb() -> ReplyKeyboardMarkup:
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
