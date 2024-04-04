from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON_COMMANDS

router = Router()


@router.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text=LEXICON_COMMANDS['no_echo'])
