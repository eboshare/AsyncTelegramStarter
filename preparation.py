import ujson

from aiogram import Bot
from addict import Dict
from motor.motor_asyncio import AsyncIOMotorClient

from utils.dispatcher import AiogramBasedDispatcher
from utils.storage import MotorStorage


CONFIG_PATH = 'config.json'
with open(CONFIG_PATH) as json_:
    config = Dict(ujson.load(json_))


bot = Bot(
    token=config.bot.token,
    proxy=config.bot.proxy,
    parse_mode=config.bot.parse_mode,
)

mongo_client = AsyncIOMotorClient(config.mongo.uri)
storage = MotorStorage(
    mongo_client=mongo_client,
    mongo_database=mongo_client[config.mongo.database]
)

dispatcher = AiogramBasedDispatcher(bot=bot, storage=storage)
