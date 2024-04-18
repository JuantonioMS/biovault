from dataclasses import dataclass, field


@dataclass
class Formula:

    sentence: str = ""
    imports: list[str] = field(default_factory = lambda: [])

    @property
    def level(self) -> str:

        if "database" in self.sentence: return "database"
        elif "register" in self.sentence: return "register"
        elif "own" in self.sentence: return "own"
        else: return "unknown"


    def __bool__(self) -> bool:
        return bool(self.sentence)