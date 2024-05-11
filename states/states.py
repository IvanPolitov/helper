from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state


class FSMWeather(StatesGroup):
    weather_settings_state = State()
    choose_locations_state = State()
    add_loc_state = State()
    choose_default_locations_state = State()
