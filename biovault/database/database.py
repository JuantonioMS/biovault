import os
import pandas as pd
from pathlib import Path
from typing import Iterator

from biovault.database.scripts import Scripts
from biovault.database.variables import Variables
from biovault.database.registers import Registers

from biovault.configuration.constants import SCRIPTS_FOLDER_NAME, VARIALBES_FOLDER_NAME, REGISTERS_FOLDER_NAME


class Database:


    def __init__(self,
                 database : Path = None,
                 scripts  : Path = None,
                 variables: Path = [],
                 registers: Path = []) -> None:

        if database is not None:
            scripts = Path(database, SCRIPTS_FOLDER_NAME)
            variables = Path(database, VARIALBES_FOLDER_NAME)
            registers = Path(database, REGISTERS_FOLDER_NAME)

        self._scripts = self._readScripts(scripts)
        self._variables = self._readVariables(variables)
        self._registers = self._readRegisters(registers)

        if self._registers is not None:
            for register in self.iterRegisters():
                register.applyFormulas(databaseLevel = True)


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Read files


    def _readScripts(self, scripts: Path) -> Scripts:

        if scripts is None: return None

        return Scripts(scripts)



    def _readVariables(self, variables: Path) -> Variables:

        if not variables: return None

        return Variables(*self._splitInputs(variables))



    def _readRegisters(self, registers: Path) -> Registers:

        if not registers: return None

        return Registers(*self._splitInputs(registers),
                         variables = self._variables)



    @staticmethod
    def _splitInputs(inputs: Path) -> list[Path]:

        if not isinstance(inputs, Path):
            return inputs

        if not inputs.is_dir(): return [inputs]
        else: return [Path(val) for sublist in [[os.path.join(i[0], j) \
                                for j in i[2]] \
                                for i in os.walk(inputs)] \
                                for val in sublist]


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Keep and drop


    def _filter(self, variable: str, sentence: str, recalculateFormulas: bool, sense: str) -> None:

        newDatabase = Database()
        if sense == "drop": newRegisters = self._registers.drop(variable, sentence, recalculateFormulas)
        elif sense == "keep": newRegisters = self._registers.keep(variable, sentence, recalculateFormulas)
        else: pass

        newDatabase._variables = self._variables
        newDatabase._registers = newRegisters
        newDatabase._scripts = self._scripts

        return newDatabase



    def drop(self, variable: str, sentence: str, recalculateFormulas = True) -> None:
        return self._filter(variable, sentence, recalculateFormulas, "drop")



    def keep(self, variable: str, sentence: str, recalculateFormulas = True) -> None:
        return self._filter(variable, sentence, recalculateFormulas, "keep")


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Iterators


    def iterConfiguration(self) -> Iterator:
        return iter(self._variables)



    def iterRegisters(self) -> Iterator:
        return iter(self._registers)


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Properties


    @property
    def _configuration(self):
        return self._variables



    @property
    def nRegisters(self) -> int:
        return len(self._registers)



    @property
    def nVariables(self) -> int:
        return len(self._variables)


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Dataframe

    def toXlsx(self, *args, name = "database.xlsx") -> None:

        if not args:
            args = self._variables.getVariablesNames()

        generalDataframe, auxDataframes = None, {}
        for arg in args:

            variable = self._variables[arg]

            if variable.type in ["object", "list"]:
                auxDataframes[variable.name] = variable.toDataframe(self._registers)

            else:
                dataframe = variable.toDataframe(self._registers)

                if generalDataframe is None:
                    generalDataframe = dataframe

                else:
                    generalDataframe = pd.concat([generalDataframe,
                                                  dataframe],
                                                 axis = "columns",
                                                 join = "inner",
                                                 ignore_index = False,
                                                 verify_integrity = True)

        with pd.ExcelWriter(name) as writer:

            generalDataframe.to_excel(writer, sheet_name = "general")

            for key, value in auxDataframes.items():
                value.to_excel(writer, sheet_name = key)



    def toDataframe(self, *args) -> pd.DataFrame:

        dataframe = None

        if not args:
            args = self._variables.getVariablesNames()

        for arg in args:

            variable = self._variables[arg]

            variableDataframe = variable.toDataframe(self._registers)

            dataframe = pd.concat([dataframe,
                                   variableDataframe],
                                  axis = "columns",
                                  join = "inner",
                                  ignore_index = False,
                                  verify_integrity = True)

        return dataframe


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Magic methods


    def __len__(self) -> int:
        return len(self._registers)




    def __iter__(self) -> Iterator:
        return self.iterRegisters()




    def __str__(self) -> str:
        msg = ["Database.",
               f"\t Registers: {self.nRegisters}",
               f"\t Variables: {self.nVariables}"]

        return "\n".join(msg)




    def __repr__(self) -> str:
        return str(self)




    def getVariable(self, variable: str):
        return self._variables[variable]