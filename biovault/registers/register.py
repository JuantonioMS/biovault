from typing import Any, Iterator
import pandas as pd

from biovault.configuration import Configuration
from biovault.validator import BioVaultValidator
from biovault.utils import Control, Rule

class Register:


    #%%  INITIALIZATION METHODS_________________________________________________________________________________________

    def __init__(self,
                 data: dict[str : Any],
                 configuration: Configuration = None) -> None:

        self._configuration = configuration

        self._data = self._readData(data)



    #%%  READ METHODS___________________________________________________________________________________________________

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



    #%%  FORMULA METHODS________________________________________________________________________________________________

    def _executeFormulas(self) -> None:

        for variable in [variable for variable in self._configuration if variable.isFormula()]:

            if variable.type == "list":
                value = variable._applyFormula(self)
                if value: self._data[variable.name] = value

            else:
                value = variable._applyFormula(self)

                if not value is None:
                    if variable.type == "object":
                        if variable.name in self._data: self._data[variable.name].update(value)
                        else: self._data[variable.name] = value

                    else: self._data[variable.name] = value



    #%%  CHECK METHODS__________________________________________________________________________________________________

    def checkRules(self,
                   configuration: Configuration = None) -> pd.DataFrame:

        schema = BioVaultValidator(configuration.jsonSchema)

        errors = sorted(schema.iter_errors(self.jsonFormat),
                        key = lambda x: x.path)

        aux = []
        for error in errors:

            name = ".".join(list(map(str,error.path)))
            if error.validator == "required":
                if name: name += "." + error.message.split(" ")[0].strip("'")
                else: name = error.message.split(" ")[0].strip("'")

            instance = error.instance if error.validator != "required" else None

            aux.append(Rule(self.id,
                            name,
                            instance,
                            error.validator,
                            error.message))

        return pd.DataFrame(aux)



    def checkControls(self,
                      configuration: Configuration = None) -> pd.DataFrame:

        aux = []
        for variable in configuration:
            for control in variable.controls:
                result = variable._evalSentence(control["control"], register = self)

                if not result is None and not result:

                    aux.append(Control(self.id,
                                      variable.name,
                                      variable.transformValueToJson(self[variable.name]),
                                      control["control"],
                                      control["message"] if "message" in control else ""))

        return pd.DataFrame(aux)



    def check(self,
              configuration: Configuration = None) -> pd.DataFrame:

        if configuration is None: configuration = self._configuration

        rules, controls = self.checkRules(configuration), self.checkControls(configuration)

        return pd.concat([rules, controls], ignore_index = True)



    #%%  PROPERTIES METHODS_____________________________________________________________________________________________

    @property
    def jsonFormat(self) -> dict[str, str | bool | int | float | list| dict]:

        aux = {"ID" : self._data["ID"]}
        for name, value in self._data.items():

            if name == "ID": continue

            aux[name] = self._configuration[name].transformValueToJson(value)

        return aux



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



    #%%  MAGIC METHODS__________________________________________________________________________________________________

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
            except KeyError: return self._configuration[index].nonDefinedValue

        else:
            raise KeyError(f"{index} is not present in this database")



    def __iter__(self) -> Iterator:
        return iter(self._data.items())