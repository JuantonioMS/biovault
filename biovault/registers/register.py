from typing import Any, Iterator
from datetime import date
import pandas as pd

from biovault.configuration import Configuration
from biovault.validator import BioVaultValidator

class Register:


    def __init__(self,
                 data: dict[str : Any],
                 configuration: Configuration = None) -> None:

        self._configuration = configuration

        self._data = self._readData(data)

        self._completeFormulas()



    def check(self,
              configuration: Configuration = None) -> dict[str : list[dict[str : Any]]]:

        if configuration is None: configuration = self._configuration

        return {"rule": self.checkRules(configuration),
                "control": self.checkControls(configuration)}


    def checkRules(self,
                   configuration: Configuration = None) -> list[dict[str : Any]]:

        if configuration is None: configuration = self._configuration

        schema = BioVaultValidator(configuration.jsonSchema)

        errors = sorted(schema.iter_errors(self.jsonDumpFormat),
                        key = lambda x: x.path)

        aux = []
        for error in errors:

            name = ".".join(list(map(str,error.path)))
            if error.validator == "required":
                if name: name += "." + error.message.split(" ")[0].strip("'")
                else: name = error.message.split(" ")[0].strip("'")

            instance = error.instance if error.validator != "required" else None

            aux.append({"variable"  : name,
                        "value"     : instance,
                        "validator" : error.validator,
                        "message"   : error.message})

        return aux



    def checkControls(self,
                      configuration: Configuration = None) -> list[dict[str : Any]]:

        if configuration is None: configuration = self._configuration

        aux = []
        for variable in configuration:
            for control in variable.controls:
                result = evalSentence(control["control"], self = self)

                if not result is None and not result:

                    aux.append({"variable"  : variable.name,
                                "value"     : variable.transformValueToJson(self[variable.name]),
                                "validator" : control["control"],
                                "message"   : control["message"] if "message" in control else ""})

        return aux



    def _completeFormulas(self) -> None:

        for variable in [variable for variable in self._configuration if variable.isFormula()]:

            value = evalSentence(variable.formula, self = self)

            if not value is None:
                self._data[variable.name] = variable.transformValueToPython(value)



    def _readData(self,
                  data: dict[str : Any]) -> dict[str : Any]:

        if not "ID" in data: raise NameError("There is no ID field in data")

        if isinstance(data["ID"], float): data["ID"] = str(int(data["ID"]))
        else: data["ID"] = str(data["ID"]).strip(" \n\r\t")

        checkedData = {"ID" : data["ID"]}
        for name, value in data.items():

            if name == "ID" or not name in self._configuration.getVariablesNames(): continue
            checkedData[name] = self._configuration[name].transformValueToPython(value)

        return checkedData



    @property
    def jsonDumpFormat(self) -> dict[str, str | bool | int | float | list| dict]:

        jsonFormat = {"ID" : self._data["ID"]}
        for name, value in self._data.items():

            if name == "ID": continue
            jsonFormat[name] = self._configuration[name].transformValueToJson(value)

        return jsonFormat



    @property
    def id(self) -> str:
        return self._data["ID"]



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



    def __getitem__(self,
                    index: str) -> Any:

        if index in self._configuration.getVariablesNames():

            try: return self._data[index]
            except KeyError: return None

        else:
            raise KeyError(f"{index} is not present in this database")



    def __iter__(self) -> Iterator:
        return iter(self._data.items())



def evalSentence(sentence, **kwargs):

    locals().update(kwargs) #  Actualiza las variables locales

    try:
        return eval(sentence)
    except (ValueError, TypeError, NameError, KeyError, IndexError):
        return None