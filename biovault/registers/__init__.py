import json
from pathlib import Path

from biovault.registers.register import Register

class Registers:

    """
    Clase de registros que alberga las registros de una base de datos.
    """

    def __init__(self, *args) -> None:

        """
        Método de inicialización.

        Args:
            *args (Path): ficheros que componen la configuración, pueden ser .xlsx o .json
        """

        self._registers = self._readArgs(*args)



    def _readArgs(self, *args) -> dict[str : Register]:

        registers = {}
        for file in args:

            with open(file, "r") as jsonFile:
                data = json.load(jsonFile)

            id = file.name.split(".")[0].split("__")[0]

            if not id in registers: registers[id] = Register(data)
            else: registers[id]._addData(data)

        return registers



    def __iter__(self):
        return iter(self._registers.values())