import pandas as pd

from biovault.database.variables.variable.type.simple.categorical import Categorical


class Nominal(Categorical):


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