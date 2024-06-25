'''
Здесь будут лежать хендлеры
для работы с настройками погоды
'''
from services.geocoding import Geocoding
from services.weather import WeatherOpenMeteo

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import or_f, and_f, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, default_state

from keyboards.weather_kb import choose_locations_kb, create_location_kb, cancel_kb, create_weather_settings_kb, cancel_kb, create_choose_default_location_kb

from states.states import FSMWeather

from database.database import user_db
from filters.handler_filter import IsLocation, IsCity

router = Router()
weather = WeatherOpenMeteo()
geocod = Geocoding()


# Обработка экрана работы со списком точек интереса
@router.message(and_f(StateFilter(FSMWeather.weather_settings_state),
                      F.text == 'Точки интереса'))
async def location_list(message: Message, state: FSMContext):
    await message.answer(text='Вы можете просмотреть или удалить локацию или добавить точку интереса',
                         reply_markup=choose_locations_kb())
    await state.set_state(state=FSMWeather.choose_locations_state)


# Просмотр списка
@ router.message(StateFilter(FSMWeather.choose_locations_state), F.text == 'Посмотреть')
async def look_list(message: Message, state: FSMContext):
    user = user_db[message.from_user.id]['locations']
    text = 'Список точек интереса:\n'
    for loc, coord in user.items():
        text += f'{str(loc)}: {str(coord)}\n'
    await message.answer(text=text, reply_markup=choose_locations_kb())


# Вернуться к списку настроек погоды
@ router.message(StateFilter(FSMWeather.choose_locations_state), F.text == 'Отмена')
async def change_weather_settings(message: Message, state: FSMContext):
    text = 'Настройки ваших прогнозов'

    await message.answer(text=text, reply_markup=create_weather_settings_kb(message.from_user.id))
    await state.set_state(state=FSMWeather.weather_settings_state)


# Удалить точку
@ router.message(StateFilter(FSMWeather.choose_locations_state), F.text == 'Удалить')
async def del_loc(message: Message, state: FSMContext):
    text = 'Выберите точку для удаления:'
    await message.answer(text=text,
                         reply_markup=create_location_kb(user_db[message.from_user.id]['locations']))


# Обработка удаления точки интереса
@ router.callback_query(StateFilter(FSMWeather.choose_locations_state), F.data.split()[0] == 'del_location')
async def del_loc_process(callback: CallbackQuery):
    loc = callback.data[13:]
    user_db[callback.from_user.id]['locations'].pop(loc)
    await callback.message.edit_reply_markup(reply_markup=create_location_kb(user_db[callback.from_user.id]['locations']))


# Добавить точку
@ router.message(StateFilter(FSMWeather.choose_locations_state), F.text == 'Добавить')
async def add_loc(message: Message, state: FSMContext):
    text = 'Напишите название города или координаты (2 числа):'
    await message.answer(text=text,
                         reply_markup=cancel_kb())
    await state.set_state(state=FSMWeather.add_loc_state)


# Обработка добавления точки интереса (отмена)
@ router.message(StateFilter(FSMWeather.add_loc_state), F.text == 'Отмена')
async def add_loc_cancel_process(message: Message, state: FSMContext):
    await message.answer(text='Вы можете просмотреть или удалить локацию или добавить точку интереса',
                         reply_markup=choose_locations_kb())
    await state.set_state(state=FSMWeather.choose_locations_state)


# Если мы напишем при добавлении точки интереса
# 2 числа, то отработает этот хэндлер и добавится точка
@ router.message(StateFilter(FSMWeather.add_loc_state), IsLocation())
async def add_location_list_by_coord(message: Message, state: FSMContext):
    string = message.text.replace(',', '.')
    latitude, longitude = tuple(map(lambda x: float(x), string.split()))
    city = geocod.find_name(latitude, longitude)
    user_db[message.from_user.id]['locations'][city] = (latitude, longitude,)
    await message.answer(text=str(city) + ' добавлен', reply_markup=choose_locations_kb())
    await state.set_state(state=FSMWeather.choose_locations_state)


# Если мы напишем при добавлении точки интереса
# текст, то отработает этот хэндлер и добавится точка
@ router.message(StateFilter(FSMWeather.add_loc_state), IsCity())
async def add_location_list_by_name(message: Message, state: FSMContext):
    city, latitude, longitude = geocod.find_coord(message.text)
    print(city, latitude, longitude)
    user_db[message.from_user.id]['locations'][city] = (latitude, longitude,)
    await message.answer(text=str(city) + ' добавлен', reply_markup=choose_locations_kb())
    await state.set_state(state=FSMWeather.choose_locations_state)


# Включить прогноз на день по часам в 8:00
@ router.message(StateFilter(FSMWeather.weather_settings_state), F.text.split(": ")[0] == 'Прогноз на день')
async def forecast_daily_active(message: Message, state: FSMContext):
    if user_db[message.from_user.id]['flag_daily_forecast']:
        user_db[message.from_user.id]['flag_daily_forecast'] = False
        text = 'Прогноз на день отключен'
    else:
        user_db[message.from_user.id]['flag_daily_forecast'] = True
        text = 'Прогноз на день включен'
    await message.answer(text=text, reply_markup=create_weather_settings_kb(message.from_user.id))


# Включить прогноз на неделю по дням в 8:00
@ router.message(StateFilter(FSMWeather.weather_settings_state), F.text.split(": ")[0] == 'Прогноз на неделю')
async def forecast_weekly_active(message: Message, state: FSMContext):
    if user_db[message.from_user.id]['flag_weekly_forecast']:
        user_db[message.from_user.id]['flag_weekly_forecast'] = False
        text = 'Прогноз на неделю отключен'
    else:
        user_db[message.from_user.id]['flag_weekly_forecast'] = True
        text = 'Прогноз на неделю включен'
    await message.answer(text=text, reply_markup=create_weather_settings_kb(message.from_user.id))


# Выбрать дефолтное место
@router.message(StateFilter(FSMWeather.weather_settings_state), F.text.split(": ")[0] == 'Дефолтное место')
async def choose_default_location(message: Message, state: FSMContext):
    text = 'Выберите место для прогноза:'
    await message.answer(text=text, reply_markup=create_choose_default_location_kb(user_db[message.from_user.id]['locations']))
    await state.set_state(state=FSMWeather.choose_default_locations_state)


# Обработка дефолтной точки
@ router.callback_query(StateFilter(FSMWeather.choose_default_locations_state), F.data.split()[0] == 'def_location')
async def def_loc_process(callback: CallbackQuery, state: FSMContext):
    user_db[callback.from_user.id]['default_location'] = callback.data[13:]
    await callback.message.answer(text='Установлено место: ' + callback.data[13:], reply_markup=create_weather_settings_kb(callback.from_user.id))
    await callback.answer()
    await state.set_state(state=FSMWeather.weather_settings_state)


# Здесь будут функции для ежедневной отправки прогноза на день и на 7 дней
async def daily_forecast(bot: Bot):
    for user in user_db:
        location = user_db[user]['default_location']
        qq = weather.get_daily_forecast(
            *user_db[user]['locations'][location])
        await bot.send_message(chat_id=user, text=qq)


async def weekly_forecast(bot: Bot):
    for user in user_db:
        location = user_db[user]['default_location']
        qq = weather.get_weekly_forecast(
            *user_db[user]['locations'][location])
        await bot.send_message(chat_id=user, text=qq)
