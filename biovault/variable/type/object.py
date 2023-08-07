from typing import Any
import pandas as pd

from biovault import Variable
from biovault.variable.type import Complex

class Object(Complex):


    def _checkRules(self, value: Any) -> list:

        checks = super()._checkRules(value)

        checks["properties"] = {}

        for variable in self.properties:
            checks["properties"][variable.name] = variable._checkRules(value[variable.name])

        return checks



    def _checkControls(self, value: Any, **kwargs) -> list:

        controls = super()._checkControls(value)

        controls["properties"] = {}
        for variable in self.properties:
            controls["properties"][variable.name] = variable._checkControls(value[variable.name], **kwargs)

        return controls


    @property
    def properties(self):

        try: return [Variable(property).getSpecificVariable() for property in self.info["properties"]]
        except KeyError: return []



    def _reduceDataframe(self,
                         dataframe: pd.DataFrame,
                         columnIdName: str) -> pd.DataFrame:

        return dataframe[[columnIdName] + [variable.sourceName for variable in self.properties]]



    def _splitIdAndValue(self,
                         row: pd.Series,
                         columnIdName: str) -> tuple:

        id = row[columnIdName]
        value = {variable.name: {"value" : row[variable.sourceName], "variable" : variable} for variable in self.properties}

        return id, value



    def _transformValue(self,
                        value: Any) -> dict:

        aux = {}
        for name, info in value.items():
            val, variable = info["value"], info["variable"]

            aux[name] = variable._transformValue(val)

        return aux