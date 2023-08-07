import json
from pathlib import Path
from typing import Any

class Register:


    def __init__(self,
                 id: str = None,
                 jsonFile: Path = None,
                 variables: object = None) -> None:

        self._data = {}

        if id is not None:
            self._id = id
            self._data["biovaultID"] = id

        if jsonFile is not None:
            self._jsonFile = jsonFile if isinstance(jsonFile, Path) else Path(jsonFile)

        if variables is not None:
            self._variables = variables


    @property
    def id(self):

        try: return self._data["biovaultID"]
        except KeyError: return self._id



    def __getattribute__(self, attr: str) -> Any:

        if attr in super().__getattribute__("_data"): return self._data[attr]
        else: return super().__getattribute__(attr)



    def addData(self,
                key: str,
                value: Any) -> None:

        if key not in self._data:
            self._data[key] = value

        else:

            if isinstance(self._data[key], list):
                self._data[key] = self._data[key] + value

            else:
                print(f"WARNING! {key} is already defined and is not a list")



    def __eq__(self, other: object) -> bool:

        if isinstance(other, Register):
            return self.id == other.id

        elif isinstance(other, str):
            return self.id == other

        else:
            return False



    def checkValues(self) -> bool:

        checks = {}
        for variable in self.variables:

            if variable.name in self._data:
                check = variable.checkValue(self._data[variable.name])

            else:
                check = variable.checkValue(None)

            checks[variable.name] = check

        return checks



    def _summarizeDict(self, dictionary) -> bool:

        flag = True
        for key, value in dictionary.items():

            if isinstance(value, bool):
                flag = flag and value

            elif isinstance(value, dict):
                flag = flag and self._summarizeDict(value)

            elif isinstance(value, list):

                auxFlag = True
                for element in value:

                    if isinstance(element, bool):
                        auxFlag = auxFlag and element

                    elif isinstance(element, dict):
                        auxFlag = auxFlag and self._summarizeDict(element)

                flag = flag and auxFlag

        return flag



    def variablesCorrect(self) -> dict:

        aux = {}
        for name, checks in self.checkValues().items():
            aux[name] = self._summarizeDict(checks)

        return aux



    def allCorrect(self) -> bool:
        return self._summarizeDict(self.variablesCorrect())



    def save(self) -> None:

        with open(f"{self.id}.json", "w") as outfile:
            json.dump(self._data, outfile, indent = 4)



    def saveSecure(self) -> None:

        aux = {}
        for name, status in self.variablesCorrect().items():
            if status:
                aux[name] = self._data[name]

        with open(f"{self.id}.json", "w") as outfile:
            json.dump(aux, outfile, indent = 4)

