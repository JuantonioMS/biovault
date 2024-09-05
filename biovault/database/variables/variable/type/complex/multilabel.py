from typing import Any
import pandas as pd

from biovault.database.variables.variable.type.complex import List


class Multilabel(List):


    def toDataframe(self, registers) -> pd.DataFrame:

        columns = list({value \
                        for register in registers \
                        for value in register[self.name]})
        columns.sort()

        data, index = [], []
        for register in registers:

            row = [False] * len(columns)

            for value in register[self.name]:
                row[columns.index(value)] = True

            data.append([";".join(sorted(register[self.name]))] + row)
            index.append(register.id)

        return pd.DataFrame(data = data,
                            index = index,
                            columns = [self.name] + [f"{self.name}.{column}" for column in columns])




    def valueToPython(self, value: Any) -> list:

        try:
            if isinstance(value, str):
                return [self.rules.items.valueToPython(element) for element in value.split(";")]
            else:
                return [str(element) for element in value]

        except ValueError: return super().valueToPython(value)