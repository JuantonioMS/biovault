from collections import UserList
from dataclasses import dataclass, field


class Controls(UserList):

    def __init__(self, *controls) -> None:
        super().__init__()

        for control in controls:
            self.append(Control(**control))




@dataclass
class Control:

    sentence: str = ""
    message: str = ""
    imports: list[str] = field(default_factory = lambda: [])
