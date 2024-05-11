from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database.database import user_db


def create_main_window_kb(user_id: int) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    if user_db[user_id]['flag_default_location']:
        weather = KeyboardButton(
            text="Погода", request_location=True
        )
    else:
        weather = KeyboardButton(
            text="Погода",
        )
    kb_builder.row(weather)
    keyboard: ReplyKeyboardMarkup = kb_builder.as_markup()
    return keyboard
