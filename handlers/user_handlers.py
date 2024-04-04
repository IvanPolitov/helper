from copy import deepcopy

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon_ru import LEXICON_COMMANDS
from aiogram.filters import Command, CommandStart
from keyboards.weather_kb import create_loc_kb, create_choose_loc_kb
from services.weather import get_weather_now
from database.database import user_db, user_dict_template


router = Router()


@router.message(Command(commands='help'))
async def call_help(message: Message):
    await message.answer(text=LEXICON_COMMANDS['/help'])


@router.message(CommandStart())
async def call_start(message: Message):
    if message.from_user.id not in user_db:
        user_db[message.from_user.id] = deepcopy(user_dict_template)
    await message.answer(text=f'Здравствуйте, {message.from_user.first_name}. {LEXICON_COMMANDS['/start']}')


@router.message(Command(commands='weather'))
async def my_location(message: Message):
    await message.answer(text='Выберите место:',
                         reply_markup=create_choose_loc_kb(
                             user_db[message.from_user.id]['locations'])
                         )
    await message.answer(text='Или отправьте свою геолокацию',
                         reply_markup=create_loc_kb())


@router.callback_query(lambda x: x.data.split()[0] == 'location')
async def send_place_weather(callback: CallbackQuery):
    qq = get_weather_now(
        float(callback.data.split()[1]), float(callback.data.split()[2]))
    await callback.message.answer(text=qq)
    await callback.answer()


@router.message(F.location)
async def send_local_weather(message: Message):
    qq = get_weather_now(message.location.latitude, message.location.longitude)
    await message.answer(text=qq)
