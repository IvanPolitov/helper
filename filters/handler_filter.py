from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsLocation(BaseFilter):
    async def __call__(self, message: Message):
        loc = message.text.replace(',', '.').split()
        if len(loc) == 2:
            try:
                loc[0] = float(loc[0])
                loc[1] = float(loc[1])
            except Exception:
                return False
            return True
        return False


class IsCity(BaseFilter):
    async def __call__(self, message: Message):
        w = all(x.isalpha() or x.isspace() or x == '-' for x in message.text)
        return w
