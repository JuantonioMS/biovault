from copy import deepcopy
import json
from pathlib import Path
import pandas as pd
from typing import Any, Iterator

from biovault.database.variables import Variables
from biovault.database.registers.register import Register
from biovault.configuration.constants import EXTENSION_VALID



class Registers:


    def __init__(self,
                 *files: Path,
                 variables: Variables = None) -> None:

        self._variables = variables

        if dict in {type(element) for element in files}:
            self._registers = self._readDictionary(files)

        else:

            self._registers = self._readFiles(*files)
            [register.applyFormulas(databaseLevel = False) for register in self]

            self._variables.addAutomaticVariables()
            [register.applyFormulas(databaseLevel = False) for register in self]




    def _readDictionary(self,
                        files: dict) -> dict[str : Register]:

        registers = {}

        for index, element in enumerate(files):

            element["ID"] = str(index)

            register = Register(element,
                                variables = self._variables,
                                registers = self)

            registers[register.id] = register

        return registers




    def _readFiles(self,
                   *args) -> dict[str : Register]:

        registers = {}
        for file in args:
            registers = self._updateRegisters(registers,
                                              self._readFile(file))

        return registers




    def _readFile(self,
                  file: Path) -> dict[str : dict[str : Register]]:

        if file.suffix not in EXTENSION_VALID: return {}


        if file.suffix == ".xlsx": return self._readExcel(file)
        elif file.suffix == ".json": return self._readJson(file)
        else: return {}




    def _readExcel(self,
                   file: Path) -> dict[str : dict[str : Register]]:

        registers = {}
        with pd.ExcelFile(file) as file:

            for sheetName in file.sheet_names:

                dataframe = file.parse(sheetName)

                for _, row in dataframe.iterrows():

                    if sheetName in self._variables.getVariablesNames(type = "list"):


                        if len(row.index) > 2:

                            register = Register({"ID" : row["ID"],
                                                 sheetName : [{column : value \
                                                               for column, value in zip(row.index, row.values) \
                                                               if column != "ID" and \
                                                                  not pd.isna(value) and \
                                                                  not (isinstance(value, str) and \
                                                                       value.lower() in ["nan", "none",
                                                                                         "ns", "nc",
                                                                                         "ns/nc", "nc/ns"])}]},
                                                variables = self._variables,
                                                registers = self)

                        else:

                            register = Register({"ID" : row["ID"],
                                                 sheetName : [value \
                                                              for column, value in zip(row.index, row.values) \
                                                              if column != "ID" and \
                                                              not pd.isna(value) and \
                                                              not (isinstance(value, str) and \
                                                                   value.lower() in ["nan", "none",
                                                                                     "ns", "nc",
                                                                                     "ns/nc", "nc/ns"])]},
                                                variables = self._variables,
                                                registers = self)

                    elif sheetName in self._variables.getVariablesNames(type = "object"):

                        register = Register({"ID" : row["ID"],
                                             sheetName : {column : value \
                                                          for column, value in zip(row.index, row.values) \
                                                          if column != "ID" and \
                                                          not pd.isna(value) and \
                                                          not (isinstance(value, str) and \
                                                               value.lower() in ["nan", "none",
                                                                                 "ns", "nc",
                                                                                 "ns/nc", "nc/ns"])}},
                                            variables = self._variables,
                                            registers = self)

                    else:

                        register = Register({column : value for column, value in zip(row.index, row.values)
                                                            if not pd.isna(value) and \
                                                            not (isinstance(value, str) and \
                                                                 value.lower() in ["nan", "none",
                                                                                   "ns", "nc",
                                                                                   "ns/nc", "nc/ns"])},
                                            variables = self._variables,
                                            registers = self)

                    registers = self._updateRegisters(registers,
                                                    {register.id : register})


        return registers




    def _readJson(self,
                  file: Path) -> dict[str : dict[str : Register]]:

        register = {}
        with open(file, "r") as file:
            data = json.load(file)

        register = Register(data, variables = self._variables, registers = self)
        return {register.id : register}




    def _updateRegisters(self,
                         currentRegisters: dict[str : Register],
                         updateRegisters: dict[str : Register]) -> dict[str : Register]:

        for updateRegisterId, updateRegister in updateRegisters.items():

            if not updateRegisterId in currentRegisters:
                currentRegisters[updateRegisterId] = updateRegister

            else:
                currentRegisters[updateRegisterId] = currentRegisters[updateRegisterId] + updateRegister

        return currentRegisters



    def getValues(self, variable: str) -> list[Any]:

        variable = self._variables[variable]

        values = []
        for register in self:

            value = register[variable.name]

            if value != variable.DEFAULT_VALUE: values.append(value)

        return values



    def _filter(self,
                variable: str,
                sentence: str,
                recalculateFormulas: bool,
                sense: str) -> list:

        bucket = []
        for register in self:

            sentenceResult = eval(sentence.replace("variable", f"register['{variable}']"))

            if sense == "keep" and sentenceResult: bucket.append(register)
            elif sense == "drop" and not sentenceResult: bucket.append(register)
            else: pass


        newRegisters = Registers(variables = self._variables)
        newRegisters._registers = {register.id : register for register in bucket}
        [setattr(register, "_registers", newRegisters) for register in newRegisters]

        if recalculateFormulas:
            [register.applyFormulas() for register in newRegisters]

        return newRegisters

    def drop(self, variable: str, sentence: str, recalculateFormulas: bool = True) -> list:
        return self._filter(variable, sentence, recalculateFormulas, "drop")

    def keep(self, variable: str, sentence: str, recalculateFormulas: bool = True) -> list:
        return self._filter(variable, sentence, recalculateFormulas, "keep")



    def __getitem__(self, value: str) -> Register:
        return self._registers[value]


    def __iter__(self) -> Iterator:
        return iter(self._registers.values())


    def __len__(self) -> int:
        return len(self._registers)