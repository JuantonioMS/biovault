import json
import pandas as pd
from pathlib import Path
from typing import Any, Iterator

from biovault.database.variables.variable import Variable
from biovault.configuration.constants import EXTENSION_VALID

class Variables:


    def __init__(self, *files: Path) -> None:

        self._variables = self._readFiles(*files)




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

        self._variables.update(newVariables)



    def _readFiles(self, *files: Path) -> dict[str, Variable]:

        variables = {}

        for file in sorted(files):
            variables.update(self._readFile(file))

        return variables




    def _readFile(self, file: Path) -> dict[str, Variable]:

        if file.suffix not in EXTENSION_VALID: return {}

        if file.suffix == ".json": return self._readJson(file)
        elif file.suffix == ".xlsx": return self._readExcel(file)
        elif file.suffix == ".tsv": return self._readTSV(file)
        else: return {}




    def _readJson(self, file: Path) -> dict[str, Variable]:


        with open(file, "r") as jsonFile: jsonInfo = json.load(jsonFile)

        if isinstance(jsonInfo, list): variables, widespread = jsonInfo, {}
        else: variables, widespread = jsonInfo["variables"], jsonInfo["widespread"]

        aux = {}
        for variable in variables:
            aux[variable["name"]] = Variable(variable, widespread = widespread).factory()

        return aux




    def _readExcel(self, file: Path) -> dict[str, Variable]:

        variables = {}
        with pd.ExcelFile(file) as file:
            for sheetName in file.sheet_names:
                variables.update(self._readSpreadsheet(file.parse(sheetName)))

        return variables




    def _readTsv(self, file: Path) -> dict[str, Variable]:

        return self._readSpreadsheet(pd.read_csv(file, sep = "\t"))




    def _readSpreadsheet(self, dataframe: pd.DataFrame) -> dict[str, Variable]:

        variables = {}
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
            variables[variable.name] = variable

        return variables




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




    def getVariables(self,
                     **filt) -> dict[str : Variable]:

        filteredVariables = {variable.name : variable for variable in self._variables.values()}

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




    def __iter__(self) -> Iterator:
        return iter(self._variables.values())




    def __getitem__(self, index: str) -> Variable:
        return self._variables[index]