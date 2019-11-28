from typing import Dict, Optional

from utils import tools
from utils.special_types import (
    StateFunction,
    UserId,
    StateString,
)


class Database:
    '''Database mock'''

    def __init__(self) -> None:
        self.storage: Dict[UserId, StateString] = {}

    async def set_state(self, user_id: UserId, state_function: StateFunction) -> None:
        fullname = tools.function_fullname(state_function)
        self.storage[user_id] = fullname

    async def get_state(self, user_id: UserId) -> Optional[StateString]:
        return self.storage.get(user_id)
