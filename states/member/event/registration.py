from typing import Optional

from aiogram.types import Message

from utils.special_types import StateFunction
from preparation import dispatcher as dp
import states.admin


@dp.state_handler(bound_handler=dp.message_handler)
async def registration_menu(message: Message) -> Optional[StateFunction]:
    await message.answer('STATE-2')
    return states.admin.admin_menu
