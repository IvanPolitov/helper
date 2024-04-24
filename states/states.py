from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state


class FSMWeather(StatesGroup):
    weather_settings = State()
    choose_locations = State()
