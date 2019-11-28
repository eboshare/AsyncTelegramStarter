from aiogram.types import Message

from preparation import dispatcher as dp
import states.admin_menu


@dp.state_handler
async def lol_function(message: Message):
    await message.answer('STATE-2')
    return states.admin_menu.some_function
