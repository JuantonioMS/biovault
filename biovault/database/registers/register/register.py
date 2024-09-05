from typing import Any, Iterator
import pandas as pd

from biovault.database.variables import Variables
#from biovault.validator import BioVaultValidator
#from biovault.utils import Control, Rule

class Register:


    def __init__(self,
                 data: dict[str : Any],
                 variables: Variables = None,
                 registers = None) -> None:

        self._variables = variables

        self._data = self._readData(data)

        self._registers = registers


#%%  FORMULAS SECTION___________________________________________________________________________________________________


    def applyFormulas(self, databaseLevel = True) -> None:

        while True:

            formulasSuccess = False

            for variable in self._variables:

                #  Si la variable no es una formula
                if not variable.isFormula(): continue

                if variable.formula.level == "database" and databaseLevel:
                    value = self._applyFormulaDatabase(variable)

                elif variable.formula.level == "register" and not variable.isAlreadyCalculated(self[variable.name]):
                    value = self._applyFormulaRegister(variable)

                elif variable.formula.level == "own" and not variable.isAlreadyCalculated(self[variable.name]):
                    value = self._applyFormulaOwn(variable)

                else:
                    value = self._applyFormulaRegister(variable)

                if value != self[variable.name]:

                    formulasSuccess = True

                    self[variable.name] = value

            if not formulasSuccess: break



    def _applyFormula(self, variable, **kwargs) -> Any:
        value = variable._applyFormula(self[variable.name],
                                       **kwargs)

        return value
    def _applyFormulaOwn(self, variable) -> Any:
        value = self._applyFormula(variable,
                                   own = self[variable.name])

        return value
    def _applyFormulaRegister(self, variable) -> Any:
        value = self._applyFormula(variable,
                                   own = self[variable.name],
                                   register = self)

        return value
    def _applyFormulaDatabase(self, variable) -> Any:
        value = self._applyFormula(variable,
                                   own = self[variable.name],
                                   register = self,
                                   database = self._registers)

        return value


#%%  READ DATA SECTION__________________________________________________________________________________________________


    def _readData(self,
                  data: dict[str : Any]) -> dict[str : Any]:

        if not "ID" in data: raise NameError("There is no ID field in data")

        if isinstance(data["ID"], float): data["ID"] = str(int(data["ID"]))
        else: data["ID"] = str(data["ID"]).strip(" \n\r\t")

        checkedData = {"ID" : data["ID"]}
        for name, value in data.items():

            if name == "ID" or not name in self._variables.getVariablesNames(): continue
            checkedData[name] = self._variables[name].valueToPython(value)

        return checkedData


#%%  PROPERTIES SECTION_________________________________________________________________________________________________


    @property
    def id(self) -> str:
        return self._data["ID"]



    @property
    def jsonFormat(self) -> dict[str, str | bool | int | float | list| dict]:

        aux = {"ID" : self._data["ID"]}
        for name, value in self._data.items():

            if name == "ID": continue

            aux[name] = self._variables[name].valueToJson(value)

        return aux


#%%  MAGIC METHODS______________________________________________________________________________________________________


    def __add__(self,
                other: Any) -> Any:

        if type(self) == type(other) and self.id == other.id:
            for name, value in other:

                if not isinstance(value, list):
                    self._data[name] = value

                else:
                    if name in self._data:
                        self._data[name] += value
                    else:
                        self._data[name] = value

        return self


    def _clean(self) -> None:

        toDelete = []
        for variable in self._variables:

            if variable.name in self._data and (self._data[variable.name] == variable.DEFAULT_VALUE or self._data[variable.name] is None):
                toDelete.append(variable.name)

        for name in toDelete:
            del self._data[name]


    def __setitem__(self, index: str, value: Any) -> None:

        self._clean()

        if index in self._variables.getVariablesNames():
            self._data[index] = self._variables[index].valueToPython(value)
        else:
            raise KeyError(f"{index} is not present in this database")



    def __getitem__(self, index: str) -> Any:

        self._clean()

        if index in self._variables.getVariablesNames():

            try: return self._data[index]
            except KeyError: return self._variables[index].DEFAULT_VALUE

        else:
            raise KeyError(f"{index} is not present in this database")



    def __iter__(self) -> Iterator:
        return iter(self._data.items())