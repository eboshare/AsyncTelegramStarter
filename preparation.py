import ujson

from aiogram import Bot
from addict import Dict

from utils.dispatcher import Dispatcher
from utils.database import Database


CONFIG_PATH = 'config.json'

with open(CONFIG_PATH) as json_:
    config = Dict(ujson.load(json_))


bot = Bot(
    token=config.token,
    proxy=config.proxy,
)

database = Database()

dispatcher = Dispatcher(
    db=database,
    bot=bot
)
