from aiogram.types import Message

from preparation import dispatcher as dp
import states.admin_menu


@dp.message_handler
async def lol_function(message: Message):
    return states.admin_menu.some_function
