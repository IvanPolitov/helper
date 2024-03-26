from aiogram import Router, F
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_COMMANDS
from aiogram.filters import Command, CommandStart
from keyboards.test import create_inline_loc

router = Router()


@router.message(Command(commands='help'))
async def call_help(message: Message):
    await message.answer(text=LEXICON_COMMANDS['/help'])


@router.message(CommandStart())
async def call_start(message: Message):
    await message.answer(text=LEXICON_COMMANDS['/start'])


@router.message(Command(commands='myloc'))
async def my_location(message: Message):
    await message.answer(text='qeqwerqw', reply_markup=create_inline_loc())


@router.message(F.location)
async def ll(message: Message):
    await message.answer(text=str(message.location.latitude) + str(message.location.longitude))
