from typing import Optional

from aiogram.types import Message

from utils.special_types import StateFunction
from preparation import dispatcher as dp
import states.member_menu.under_member.voobshe_lol


@dp.state_handler
@dp.primary_state
async def some_function(message: Message) -> Optional[StateFunction]:
    await message.answer('STATE-1')
    return states.member_menu.under_member.voobshe_lol.lol_function
