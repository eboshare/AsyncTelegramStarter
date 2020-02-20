from typing import Optional

from aiogram.types import Message

from utils.special_types import StateFunction
from preparation import dispatcher as dp
# import states.admin
import states.member.checkin


@dp.state_handler(bound_handler=dp.message_handler)
async def registration_menu(message: Message) -> Optional[StateFunction]:
    await message.answer('STATE-2')
    return states.member.checkin.checkin_menu
