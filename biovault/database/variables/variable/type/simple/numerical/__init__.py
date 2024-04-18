from typing import Any

from biovault.database.variables.variable.type.simple import Simple


class Numerical(Simple):


    @property
    def jsonSchema(self) -> dict[str, Any]:

        schema = super().jsonSchema

        schema["type"] = "number"

        return schema



    @classmethod
    def transformValueToPython(cls, value: Any) -> float:

        try: return float(value)
        except (ValueError, TypeError): return super().transformValueToPython(value)


from biovault.database.variables.variable.type.simple.numerical.float import Float
from biovault.database.variables.variable.type.simple.numerical.integer import Integer
from biovault.database.variables.variable.type.simple.numerical.percentage import Percentage
from biovault.database.variables.variable.type.simple.numerical.date import Date