from typing import (
    Any,
    List,
    Dict,
    Optional,
)
from pathlib import Path
import inspect

import aiogram
from aiogram.types import Update

from utils import tools
from utils.special_types import StateFunction
from utils.database import Database


def importtable_names(path: Path, suffix: str = '.py') -> List[str]:
    result = []
    for item in path.rglob(f'*{suffix}'):
        string_path = str(item)
        string_path = string_path.replace('.py', '').replace('/', '.')
        result.append(string_path)
    return result


class Dispatcher:
    DEFAULT_DIR: str = 'states'
    DICT_HANDLER: Dict[Optional[str], StateFunction] = {}

    def __init__(self, db: Database, bot: aiogram.Bot, *args: Any, **kwargs: Any) -> None:
        self.db = db
        self.bot = bot
        self.aiogram_dispatcher = aiogram.Dispatcher(*args, **kwargs, bot=bot)
        self.aiogram_dispatcher.updates_handler.register(handler=self._update_handler, index=0)

    async def _update_handler(self, update: Update) -> None:
        next_state = None
        try:
            if update.message:
                user_id = update.message.chat.id
                state_string = await self.db.get_state(user_id)
                if state_string is None and None not in self.DICT_HANDLER:
                    raise RuntimeError('primary state isn\'t defined')
                else:
                    state_function = self.DICT_HANDLER[state_string]
                    next_state = await state_function(update.message)

        except Exception as error:
            raise error  # [debug] в будущем тут будет логирование ошибки

        finally:
            if inspect.iscoroutinefunction(next_state):
                await self.db.set_state(user_id, next_state)

    def primary_state(self, state_function: StateFunction) -> StateFunction:
        """
        Добавляет току входа - состояние с названием None

        :param state_function: функция-состояние
        :type state_function: StateFunction
        :return: та же самая функция-состояние
        :rtype: StateFunction
        """
        self.DICT_HANDLER[None] = state_function
        return state_function

    def state_handler(self, state_function: StateFunction) -> StateFunction:
        # NOTE: тестовый вид, дальше будет уровень вложенности с аргументами
        state_fullname = tools.function_fullname(state_function)
        self.DICT_HANDLER[state_fullname] = state_function
        print(f'DEBUG: {state_fullname}')  # DEBUG
        return state_function

    def import_states(self) -> None:
        path = Path(self.DEFAULT_DIR)
        paths = importtable_names(path)
        for name in paths:
            __import__(name)

    def start_polling(self) -> None:
        self.import_states()
        # BUG: почему-то не печатается статус запуска на экран
        aiogram.executor.start_polling(dispatcher=self.aiogram_dispatcher)
