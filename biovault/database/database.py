import pandas as pd
from pathlib import Path


class Database:


    def __init__(self,
                 databases: list,
                 variables,
                 id: str) -> None:

        self.variables = variables

        self.id = id

        self.databases = self._formatDatabases(databases)

        self.registers = self._extractRegisters()



    def _formatDatabases(self, databases) -> dict:

        auxDatabases = {}
        for database in databases:

            if not isinstance(database, Path):
                database = Path(database)

            auxDatabases[database.name] = database

        return auxDatabases



    def _extractRegisters(self) -> dict:

        from biovault.register import Register
        from biovault import Registers

        registers = Registers()
        for variable in self.variables:

            registers = variable._extractData(self.databases,
                                              self.id,
                                              registers)

        return registers