from preparation import dispatcher as dp
import states.member_menu.under_member.voobshe_lol


@dp.message_handler
async def some_function():
    return states.member_menu.under_member.voobshe_lol.lol_function
