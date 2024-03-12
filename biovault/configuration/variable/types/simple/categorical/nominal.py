import pandas as pd
from typing import Any
from biovault.configuration.variable.types.simple.categorical import Categorical

class Nominal(Categorical):


    def _completeVariableInfo(self,
                              variable: dict[str : Any],
                              widespread: dict[str : Any]) -> dict[str : Any]:

        variable = super()._completeVariableInfo(variable, widespread)

        if "enum" in variable["rules"] and isinstance(variable["rules"]["enum"], str):
            variable["rules"]["enum"] = ";".split(variable["rules"]["enum"])

        return variable



    def variableToDataframe(self, registers) -> pd.DataFrame:

        columns = list({register[self.name] for register in registers if not register[self.name] is None})
        columns.sort()

        data, index = [], []
        for register in registers:

            row = [False] * len(columns)

            if not register[self.name] is None:
                row[columns.index(register[self.name])] = True

            else:
                row = [None] * len(columns)

            data.append(row)
            index.append(register.id)

        return pd.DataFrame(data = data,
                            index = index,
                            columns = [f"{self.name}.{column}" for column in columns])