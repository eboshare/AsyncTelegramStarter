from typing import Optional

from aiogram.types import Message

from utils.special_types import StateFunction
from preparation import dispatcher as dp


@dp.state_handler(bound_handler=dp.message_handler)
async def checkin_menu(message: Message) -> Optional[StateFunction]:
    pass
