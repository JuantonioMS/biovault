from pathlib import Path
from typing import Any

from biovault import Register

class Registers:


    def __init__(self,
                 registers: list = None,
                 directory: Path = None) -> None:

        self._registers = []



    def addRegister(self, register: Register) -> None:
        self._registers.append(register)



    def __iter__(self):
        return iter(self._registers)



    def __getitem__(self, item) -> Any:
        return next(filter(lambda x: x.id == item, self._registers))
