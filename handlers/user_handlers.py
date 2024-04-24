from copy import deepcopy

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon_ru import LEXICON_COMMANDS
from aiogram.filters import Command, CommandStart, StateFilter, or_f, and_f
from keyboards.weather_kb import create_weather_settings_kb, create_location_kb, choose_locations_kb, cancel_locations_kb
from services.weather import WeatherOpenMeteo
from services.find_city import City
from database.database import user_db, user_dict_template
from states.states import FSMWeather
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from filters.handler_filter import IsLocation, IsCity

router = Router()
weather = WeatherOpenMeteo()
city = City()
# Дефолтные команды


@router.message(Command(commands='help'))
async def call_help(message: Message):
    await message.answer(text=LEXICON_COMMANDS['/help'])


@router.message(CommandStart())
async def call_start(message: Message):
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(user_dict_template)
    await message.answer(text=f'Здравствуйте, {message.from_user.first_name}. {LEXICON_COMMANDS['/start']}')


# Когда мы будем настраивать нашу погоду
# мы будем входить в состояние нестояния

# Выводим список настроек погоды


@router.message(Command(commands='weather_settings'))
async def change_weather_settings(message: Message, state: FSMContext):
    text = 'Настройки ваших прогнозов'

    await message.answer(text=text,
                         reply_markup=create_weather_settings_kb())
    await state.set_state(state=FSMWeather.weather_settings)

# Выводим список инлайн-кнопок мест для просмотра погоды


@router.message(or_f(and_f(StateFilter(FSMWeather.weather_settings), F.text == 'Точки интереса'),
                and_f(StateFilter(FSMWeather.choose_locations), F.text == 'Отмена')))
async def location_list(message: Message, state: FSMContext):
    await message.answer(text='Вы можете просмотреть, добавить или удалить локацию',
                         reply_markup=choose_locations_kb())
    await message.answer(text='из списка ниже:', reply_markup=create_location_kb(user_db[message.from_user.id]['locations']))
    await state.set_state(state=FSMWeather.choose_locations)


@router.message(StateFilter(FSMWeather.choose_locations), F.text == 'Добавить')
async def edit_location_list(message: Message, state: FSMContext):
    text = 'Напишите название населенного пункта или координаты места (координаты работают точнее)'
    await message.answer(text=text, reply_markup=cancel_locations_kb())


@router.message(StateFilter(FSMWeather.choose_locations), IsLocation())
async def add_location_list(message: Message, state: FSMContext):
    string = message.text.replace(',', '.')

    latitude, longitude = string.split()
    qq = weather.get_current_weather(float(latitude), float(longitude))
    await message.answer(text=qq, reply_markup=create_weather_settings_kb())
    await state.set_state(state=FSMWeather.weather_settings)


@router.message(StateFilter(FSMWeather.choose_locations), IsCity())
async def add_location_list(message: Message, state: FSMContext):
    latitude, longitude = city.find(message.text)
    qq = weather.get_current_weather(latitude, longitude)
    await message.answer(text=qq, reply_markup=create_weather_settings_kb())
    await state.set_state(state=FSMWeather.weather_settings)


'''@router.message(F.text)
async def send_city_weather(message: Message):
    city = City()
    latitude, longitude = city.find(message.text)

    qq = weather.get_current_weather(latitude, longitude)
    await message.answer(text=qq)
    
@router.message(Command(commands='weather'))
async def my_location(message: Message):
    await message.answer(text='Выберите место:',
                         reply_markup=create_choose_loc_kb(
                             user_db[message.from_user.id]['locations'])
                         )
    await message.answer(text='Или отправьте свою геолокацию',
                         reply_markup=create_loc_kb())
                         '''
