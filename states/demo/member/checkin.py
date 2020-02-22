from typing import Optional

from aiogram.types import Message

from utils.special_types import StateFunction
from preparation import dispatcher as dp
import states.demo.admin


@dp.state_handler(bound=dp.message_handler)
async def checkin_menu(message: Message) -> Optional[StateFunction]:
    await message.answer('STATE-3')
    return states.demo.admin.admin_menu
