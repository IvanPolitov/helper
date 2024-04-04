from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_RU


def create_loc_kb(*args) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.row(
        KeyboardButton(
            text=LEXICON_RU['get_geo_button'],
            request_location=True,
        )
    )
    keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(resize_keyboard=True)
    return keyboard


def create_choose_loc_kb(args) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for button in args:
        kb_builder.row(
            InlineKeyboardButton(
                text=button,
                callback_data=f'location {str(args[button][0])} {str(args[button][1])}')
        )

    keyboard: InlineKeyboardMarkup = kb_builder.as_markup(resize_keyboard=True)
    return keyboard
