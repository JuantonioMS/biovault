from typing import Any, Union

from biovault.database.variables.variable.type.simple.numerical import Numerical

class Integer(Numerical):


    @property
    def jsonSchema(self) -> dict[str, Any]:

        schema = super().jsonSchema

        schema["type"] = "integer"

        return schema


    @classmethod
    def transformValueToPython(cls, value: Any) -> Union[int, Any]:

        try: return int(value)
        except (ValueError, TypeError): return super().transformValueToPython(value)