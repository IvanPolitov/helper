from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsLocation(BaseFilter):
    async def __call__(self, message: Message):
        w = all(x.isdigit() or x.isspace() or x ==
                ',' or x == '.'for x in message.text)
        return w


class IsCity(BaseFilter):
    async def __call__(self, message: Message):
        w = all(x.isalpha() or x.isspace() or x == '-' for x in message.text)
        return w
