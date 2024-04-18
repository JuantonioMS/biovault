from dataclasses import dataclass, field


class Controls(list):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        for index in range(len(self)):
            content = self.__getitem__(index)
            self.__setitem__(index, Control(**content))



@dataclass
class Control:

    sentence: str = ""
    message: str = ""
    imports: list[str] = field(default_factory = lambda: [])
