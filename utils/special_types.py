# import types
from typing import (
    Callable,
    # Union,
    # TypeVar,
    Awaitable,
)

# возможно нужно убрать возможность возвращать строку в виде состояния
StateString = str
StateFunction = Callable[..., Awaitable]

# identifiers
UserId = int
