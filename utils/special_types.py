# import types
from typing import (
    Callable,
    # Union,
    # TypeVar,
    Awaitable,
)

StateString = str
StateFunction = Callable[..., Awaitable]

UserId = int
