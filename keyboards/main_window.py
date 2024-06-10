from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from database.database import user_db


def create_main_window_kb(user_id: int) -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    weather = KeyboardButton(
        text="Погода",
    )
    kb_builder.row(weather)
    keyboard: ReplyKeyboardMarkup = kb_builder.as_markup()
    return keyboard
