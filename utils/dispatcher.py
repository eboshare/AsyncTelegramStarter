from typing import (
    Any,
    # List,
    Dict,
    Optional,
    Iterator,
    TypeVar,
    Awaitable,
)
import types
from pathlib import Path
import inspect
import functools

import aiogram
from aiogram.types import Update
from types import FunctionType

from utils import tools
from utils.special_types import StateFunction
from utils.database import Database


def py_file_names(path: Path, suffix: str = '.py') -> Iterator[str]:
    for item in path.rglob(f'*{suffix}'):
        string_path = str(item)
        yield string_path.replace('.py', '').replace('/', '.')


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
                state_value = await self.db.get_state(user_id)
                if state_value is None and None not in self.DICT_HANDLER:
                    raise RuntimeError('primary state isn\'t defined')
                else:
                    state_function = self.DICT_HANDLER[state_value]
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
        for name in py_file_names(path):
            __import__(name)

    def start_polling(self) -> None:
        self.import_states()
        # BUG: почему-то не печатается статус запуска на экран от aiogram
        aiogram.executor.start_polling(dispatcher=self.aiogram_dispatcher)


class AiogramBasedDispatcher(aiogram.Dispatcher):
    __DEFAULT_DIR: str = 'states'

    def __init__(self, storage, *args: Any, **kwargs: Any) -> None:
        self.__db = storage
        return super().__init__(*args, storage=storage, **kwargs)

    def __state_switcher(self, callback: FunctionType) -> FunctionType:

        @functools.wraps(callback)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            user = aiogram.types.User.get_current()  # NOTE: возможно не самый лучший вариант
            result = await callback(*args, **kwargs)
            if inspect.iscoroutinefunction(result):
                state = tools.function_fullname(result)
                await self.__db.set_state(user=user.id, state=state)
                print(self.__db.data)  # DEBUG

            return result

        return wrapper

    def state_handler(
            self,
            *,
            primary_state: bool = False,
            bound_handler: FunctionType = aiogram.Dispatcher.message_handler,
            **kwargs: Any) -> FunctionType:

        def wrapper(callback: FunctionType) -> FunctionType:
            states = []
            state = locals().get('state') or tools.function_fullname(callback)
            states.append(state)

            callback = self.__state_switcher(callback)
            if primary_state:
                states.append(None)

            for state in states:
                handler = bound_handler(state=state, **kwargs)
                result = handler(callback)
            return result

        return wrapper

    def __import_states(self) -> None:
        path = Path(self.__DEFAULT_DIR)
        for name in py_file_names(path):
            __import__(name)

    async def start_polling(self, *args: Any, **kwargs: Any) -> Any:
        self.__import_states()
        return await super().start_polling(*args, **kwargs)
