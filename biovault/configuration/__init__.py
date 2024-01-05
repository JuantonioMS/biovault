import pandas as pd
import json
from pathlib import Path

from biovault.configuration.variable  import Variable

class Configuration:

    """
    Clase de configuración que alberga las normas de una base de datos.
    """

    def __init__(self, *args) -> None:

        """
        Método de inicialización.

        Args:
            *args (Path): ficheros que componen la configuración, pueden ser .xlsx o .json
        """

        variables = []
        for file in args:

            if file.suffix == ".json":
                variables += self._readJson(file)

            elif file.suffix == ".xlsx":
                variables += self._readExcel(file)

        self._variables = variables



    def _readExcel(self,
                   file: Path) -> list:

        df = pd.read_excel(file)

        variables = []
        for _, row in df.iterrows():
            aux = {}
            for col in row.index:

                if pd.isna(row[col]): continue

                if "." in col:

                    field, name = col.split(".")
                    if not field in aux: aux[field] = {}

                    aux[field][name] = row[col]

                else: aux[col] = row[col]

            variables.append(Variable(aux).fabrica())

        return variables



    def _readJson(self,
                  file: Path) -> list:

        with open(file, "r") as jsonFile:
            variables = json.load(jsonFile)

        return [Variable(variable).fabrica() for variable in variables]



    def jsonSchema(self) -> dict:

        schema = {"type" : "object",
                  "properties" : {"ID" : {}},
                  "required" : ["ID"],
                  "additionalProperties": False}

        for variable in self._variables:

            schema["properties"][variable.name] = variable.jsonSchema

            if variable._variable["rules"]["required"]:
                schema["required"].append(variable.name)

        return schema



    def save(self,
             file: Path) -> None:

        with open(file, "w") as outfile:
            json.dump([variable.jsonDumpFormat for variable in self._variables],
                      outfile,
                      ensure_ascii = False,
                      indent = "    ")