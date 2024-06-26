from typing import Any
import pandas as pd

from biovault.database.variables.variable.type.complex import List


class Multilabel(List):


    def variableToDataframe(self, registers) -> pd.DataFrame:

        columns = list({value \
                        for register in registers \
                        for value in register[self.name]})
        columns.sort()

        data, index = [], []
        for register in registers:

            row = [False] * len(columns)

            for value in register[self.name]:
                row[columns.index(value)] = True

            data.append(row)
            index.append(register.id)

        return pd.DataFrame(data = data,
                            index = index,
                            columns = [f"{self.name}.{column}" for column in columns])




    def transformValueToPython(self, value: Any) -> list:

        try:
            if isinstance(value, str):
                return [self.rules.items.transformValueToPython(element) for element in value.split(";")]
            else:
                return [str(element) for element in value]

        except ValueError: return super().transformValueToPython(value)