import pandas as pd
from typing import Any

from biovault.database.variables.variable.type.simple.categorical import Ordinal


class Ranking(Ordinal):


    @property
    def jsonSchema(self) -> dict:

        schema = super().jsonSchema
        schema["type"] = "integer"
        return schema



    @classmethod
    def valueToPython(cls, value: Any) -> int:

        try: return int(value)
        except (ValueError, TypeError): return super().valueToPython(value)



    def toDataframe(self, registers) -> pd.DataFrame:
        return self.__class__.__mro__[6].toDataframe(self, registers)