from typing import Any
import pandas as pd

from biovault.variable import Variable


class Object(Variable):


    def _reduceDataframe(self,
                         dataframe: pd.DataFrame,
                         columnIdName: str) -> pd.DataFrame:

        return dataframe[[columnIdName] + [variable.sourceName for variable in self.values]]



    def _splitIdAndValue(self,
                         row: pd.Series,
                         columnIdName: str) -> tuple:

        id = row[columnIdName]
        value = {variable.name: {"value" : row[variable.sourceName], "variable" : variable} for variable in self.values}

        return id, value



    def _transformValue(self,
                        value: Any) -> dict:

        aux = {}
        for name, info in value.items():
            val, variable = info["value"], info["variable"]

            aux[name] = variable._transformValue(val)

        return aux