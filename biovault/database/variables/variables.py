from collections import UserDict
import json
import pandas as pd
from pathlib import Path
from typing import Any, Iterator

from biovault.database.variables.variable import Variable
from biovault.configuration.constants import EXTENSION_VALID


class Variables(UserDict):


    def __init__(self, *files: Path | dict) -> None:
        super().__init__()

        if dict in {type(element) for element in files}:

            for element in files:
                variable = Variable(element).factory()
                self[variable.name] = variable

        else:
            self._readFiles(*files)


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Read files


    def _readFiles(self, *files: Path) -> None:
        for file in sorted(files): self._readFile(file)




    def _readFile(self, file: Path) -> None:

        if file.suffix == ".json": self._readJson(file)
        elif file.suffix == ".xlsx": self._readExcel(file)
        elif file.suffix == ".tsv": self._readTSV(file)
        else: pass




    def _readJson(self, file: Path) -> None:

        with open(file, "r") as infile: info = json.load(infile)

        if isinstance(info, list): variables, widespread = info, {}
        else: variables, widespread = info["variables"], info["widespread"]

        for variable in variables:
            variable = Variable(variable, widespread = widespread).factory()
            self[variable.name] = variable




    def _readExcel(self, file: Path) -> None:

        with pd.ExcelFile(file) as infile:
            for sheetName in infile.sheet_names:
                self._readSpreadsheet(infile.parse(sheetName))




    def _readTsv(self, file: Path) -> None:
        self._readSpreadsheet(pd.read_csv(file, sep = "\t"))




    def _readSpreadsheet(self, dataframe: pd.DataFrame) -> None:

        for _, row in dataframe.iterrows():

            aux = {}
            for col in row.index:

                if pd.isna(row[col]): continue

                if "." in col:

                    field, name = col.split(".")
                    if not field in aux: aux[field] = {}

                    aux[field][name] = row[col]

                else: aux[col] = row[col]

            variable = Variable(aux).factory()
            self[variable.name] = variable


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region JSON schema


    @property
    def jsonSchema(self) -> dict[str : Any]:

        schema = {"type" : "object",
                  "properties" : {"ID" : {"type" : "string"}},
                  "required" : ["ID"],
                  "additionalProperties": False}

        for variable in self:

            schema["properties"][variable.name] = variable.jsonSchema

            if variable.rules.required:
                schema["required"].append(variable.name)

        return schema


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Getters


    def getVariables(self,
                     **filt) -> dict[str : Variable]:

        filteredVariables = {variable.name : variable for variable in self.data.values()}

        for filtName, filtValue in filt.items():

            if isinstance(filtValue, (tuple, list, set)):

                filteredVariables = {variable.name : variable \
                                     for variable in filteredVariables.values()\
                                     if not any([not element in getattr(variable, filtName) \
                                                 for element in filtValue])}

            else:

                filteredVariables = {variable.name : variable \
                                     for variable in filteredVariables.values()\
                                     if filtValue == getattr(variable, filtName)}

        return filteredVariables



    def getVariablesNames(self,
                          **filt) -> list[str]:
        return list(self.getVariables(**filt).keys())


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Magic methods


    def __iter__(self) -> Iterator:
        return iter(self.data.values())


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region TODO


    def addAutomaticVariables(self) -> None:

        newVariables = {}

        for variable in self:

            if variable.type == "multilabel":

                newVariable = Variable({"name": f"{variable.name}_length",
                                        "type": "integer",
                                        "formula": f"len(register['{variable.name}'])"}).factory()

                newVariables[newVariable.name] = newVariable

                newVariable = Variable({"name": f"{variable.name}_bool",
                                        "type": "boolean",
                                        "formula": f"bool(register['{variable.name}'])"}).factory()

                newVariables[newVariable.name] = newVariable

        self.update(newVariables)