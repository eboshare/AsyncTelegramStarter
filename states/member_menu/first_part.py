from typing import Optional

from aiogram.types import Message

from utils.special_types import StateFunction
from preparation import dispatcher as dp


@dp.state_handler
async def lalala_function(message: Message) -> Optional[StateFunction]:
    pass
