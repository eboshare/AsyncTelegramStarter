from typing import Optional

from aiogram.types import Message

from utils.special_types import StateFunction
from preparation import dispatcher as dp
import states.demo.member.event.registration


@dp.state_handler(primary_state=True, bound=dp.message_handler)
async def admin_menu(message: Message) -> Optional[StateFunction]:
    await message.answer('STATE-1')
    return states.demo.member.event.registration.registration_menu
