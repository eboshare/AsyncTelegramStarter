import ujson

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from addict import Dict


from utils.dispatcher import Dispatcher, AiogramBasedDispatcher
from utils.database import Database


CONFIG_PATH = 'config.json'

with open(CONFIG_PATH) as json_:
    config = Dict(ujson.load(json_))


bot = Bot(
    token=config.token,
    proxy=config.proxy,
)

database = Database()

# dispatcher = Dispatcher(
#     db=database,
#     bot=bot
# )


storage = MemoryStorage()

dispatcher = AiogramBasedDispatcher(
    # db=database,
    bot=bot,
    storage=storage,
)
