import pandas as pd
from typing import Any, Union

from biovault.database.variables.variable.type.simple.categorical import Ordinal


class Ranking(Ordinal):

    @property
    def jsonSchema(self) -> dict[str : Any]:

            schema = super().jsonSchema

            schema["type"] = "integer"

            return schema



    def transformValueToPython(self, value: Any) -> int:

        try: return int(value)
        except (ValueError, TypeError): return super().transformValueToPython(value)



    def variableToDataframe(self, registers) -> pd.DataFrame:

        return pd.DataFrame(data = [register[self.name] for register in registers],
                            index = [register.id for register in registers],
                            columns = [self.name])