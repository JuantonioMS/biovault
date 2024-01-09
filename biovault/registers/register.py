from typing import Any, Iterator
from datetime import date
import pandas as pd

from biovault.configuration import Configuration

class Register:


    def __init__(self,
                 data: dict[str : Any],
                 configuration: Configuration = None) -> None:

        self._configuration = configuration

        self._data = self._readData(data)


    def _readData(self,
                  data: dict[str : Any]) -> dict[str : Any]:

        if not "ID" in data: raise NameError("There is no ID field in data")

        if isinstance(data["ID"], float): data["ID"] = str(int(data["ID"]))
        else: data["ID"] = str(data["ID"])

        checkedData = {"ID" : data["ID"]}
        for name, value in data.items():

            if name == "ID": continue
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
