import pandas as pd

from biovault.database.variables.variable.type.simple.categorical import Categorical


class Nominal(Categorical):


    def toDataframe(self, registers) -> pd.DataFrame:

        classes = list({register[self.name] \
                        for register in registers \
                        if register[self.name] is not None})
        classes.sort()

        index, data = [], []
        for register in registers:

            value = register[self.name]

            if value is not None: row = [True if value == clas else False for clas in classes]
            else: row = [None] * len(classes)

            index.append(register.id); data.append(row)

        return pd.concat([super().toDataframe(registers),
                          pd.DataFrame(data = data,
                                       index = index,
                                       columns = [f"{self.name}.{clas}" for clas in classes])],
                         axis = "columns",
                         join = "inner",
                         ignore_index = False,
                         verify_integrity = True)