# import types
from typing import (
    Callable,
    Union,
    Awaitable,
)

# возможно нужно убрать возможность возвращать строку в виде состояния
StateString = str
StateFunction = Callable[..., Union[StateString, Awaitable]]
