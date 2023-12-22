from pathlib import Path
from typing import Union

from biovault.configuration import Configuration
from biovault.registers import Registers
class Database:


    def __init__(self,
                 configuration: Union[Path, list[Path]] = None,
                 registers: Union[Path, list[Path]] = None) -> None:

        self._configuration = self._readConfiguration(configuration)
        self._registers = self._readRegisters(registers)



    def _readConfiguration(self, configuration: Union[Path, list[Path]]) -> Configuration:

        if configuration.is_dir():
            return Configuration(*list(configuration.iterdir()))
        else:
            return Configuration(*configuration)



    def _readRegisters(self, registers: Union[Path, list[Path]]) -> Registers:
        pass