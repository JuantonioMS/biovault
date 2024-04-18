from dataclasses import dataclass, field


@dataclass
class Info:

    description: str = ""
    groups: set[str] = field(default_factory = lambda: set())
    longName: str = ""