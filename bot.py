from aiogram import executor

from preparation import dispatcher as dp


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp)
