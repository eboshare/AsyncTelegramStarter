from typing import (
    Any,
    List,
    Dict,
)
from pathlib import Path

from utils.special_types import StateFunction


def importtable_names(path: Path, suffix: str = '.py') -> List[str]:
    result = []
    for item in path.rglob(f'*{suffix}'):
        string_path = str(item)
        string_path = string_path.replace('.py', '').replace('/', '.')
        result.append(string_path)
    return result


class Dispatcher:
    DEFAULT_DIR: str = 'states'
    DICT_HANDLER: Dict[str, StateFunction] = {}

    def message_handler(self, state_function: StateFunction) -> StateFunction:
        # NOTE: тестовый вид, дальше будет уровень вложенности с аргументами
        state_fullname = f'{state_function.__module__}.{state_function.__name__}'
        self.DICT_HANDLER[state_fullname] = state_function
        print(state_fullname)  # DEBUG
        return state_function

    def start_polling(self, *args: Any, **kwargs: Any) -> None:
        path = Path(self.DEFAULT_DIR)
        paths = importtable_names(path)
        for name in paths:
            __import__(name)
        # NOTE: дальше идет запуск полинга aiogram и запуск fsm
