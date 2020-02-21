import importlib
from typing import (
    Any,
    # List,
    # Dict,
    # Optional,
    Iterator,
    # TypeVar,
    # Awaitable,
)
# import types
from pathlib import Path
import inspect
import functools

import aiogram
from types import FunctionType

from utils import tools


def module_names(path: Path, suffix: str = '.py') -> Iterator[str]:
    suffix_length = len(suffix)
    for item in path.rglob(f'*{suffix}'):
        if item.is_file():
            parts = list(item.parts)
            parts[-1] = item.name[:-suffix_length]  # cut off suffix
            yield '.'.join(parts)


class AiogramBasedDispatcher(aiogram.Dispatcher):
    # NOTE: not the best name

    def __init__(self, *args: Any, states_directory: str = 'states', **kwargs: Any) -> None:
        self.__states_directory = states_directory
        return super().__init__(*args, **kwargs)

    def __state_switcher(self, callback: FunctionType) -> FunctionType:

        @functools.wraps(callback)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            chat = aiogram.types.Chat.get_current()
            user = aiogram.types.User.get_current()  # NOTE: maybe not the best way
            result = await callback(*args, **kwargs)
            if inspect.iscoroutinefunction(result):
                state = tools.function_fullname(result)
                await self.storage.set_state(user=user.id, chat=chat.id, state=state)

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
        path = Path(self.__states_directory)
        for name in module_names(path):
            importlib.import_module(name=name)

    async def start_polling(self, *args: Any, **kwargs: Any) -> Any:
        self.__import_states()
        return await super().start_polling(*args, **kwargs)
