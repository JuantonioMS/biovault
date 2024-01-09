import pandas as pd
import json
from pathlib import Path
from typing import Any, Iterator

from biovault.configuration.variable  import Variable

class Configuration:

    """
    Clase de configuración que alberga las normas de una base de datos.
    """

    def __init__(self,
                 *args) -> None:

        """
        Método de inicialización.

        Args:
            *args (Path): ficheros que componen la configuración, pueden ser .xlsx o .json
        """

        self._variables = self._readFiles(*args)



    def _readFiles(self,
                   *args) -> dict[str : Variable]:

        variables = {}
        for file in args:
            variables.update(self._readFile(file))

        return variables



    def _readFile(self,
                  file: Path) -> dict[str : Variable]:

        if file.suffix == ".json": return self._readJson(file)
        elif file.suffix == ".xlsx": return self._readExcel(file)
        elif file.suffix == ".tsv": return self._readTSV(file)
        else: raise TypeError(f"{file.suffix} extension not valid")



    def _readJson(self,
                  file: Path) -> dict[str : Variable]:

        with open(file, "r") as jsonFile: variables = json.load(jsonFile)

        return {variable.name : variable for variable in [Variable(variable).fabrica() for variable in variables]}



    def _readExcel(self,
                   file: Path) -> dict[str : Variable]:

        variables = {}
        with pd.ExcelFile("tests/material/registers/xlsx/registers.xlsx") as file:
            for sheetName in file.sheet_names:
                variables.update(self._readSpreadSheet(file.parse(sheetName)))

        return variables



    def _readTSV(self,
                 file: Path) -> dict[str : Variable]:
        return self._readSpreadSheet(pd.read_csv(file, sep = "\t"))



    def _readSpreadSheet(self,
                         dataframe: pd.DataFrame) -> dict[str : Variable]:

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

            variable = Variable(aux).fabrica()
            variables[variable.name] = variable

        return variables



    def save(self,
             file: Path) -> None:

        with open(file, "w") as outfile:
            json.dump([variable.jsonDumpFormat for variable in self._variables],
                      outfile,
                      ensure_ascii = False,
                      indent = "    ")



    def getVariables(self,
                     **filt) -> dict[str : Variable]:

        filteredVariables = {variable.name : variable for variable in self._variables.values()}
        for filtName, filtValue in filt.items():

            if isinstance(filtValue, (tuple, list, set)):
                filteredVariables = {variable.name : variable for variable in filteredVariables.values()\
                                     if not any([not element in getattr(variable, filtName) for element in filtValue])}

            else:
                filteredVariables = {variable.name : variable for variable in filteredVariables.values()\
                                     if filtValue == getattr(variable, filtName)}

        return filteredVariables



    def getVariablesNames(self,
                          **filt) -> list[str]:
        return list(self.getVariables(**filt).keys())



    @property
    def jsonSchema(self) -> dict[str : Any]:

        schema = {"type" : "object",
                  "properties" : {"ID" : {"type" : "string"}},
                  "required" : ["ID"],
                  "additionalProperties": False}

        for variable in self:

            schema["properties"][variable.name] = variable.jsonSchema

            if variable._variable["rules"]["required"]:
                schema["required"].append(variable.name)

        return schema



    def __iter__(self) -> Iterator:
        return iter(self._variables.values())



    def __getitem__(self,
                    index: str) -> Variable:
        return self._variables[index]