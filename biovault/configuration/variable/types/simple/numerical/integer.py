from typing import Any, Union

from biovault.configuration.variable.types.simple.numerical import Numerical

class Integer(Numerical):

    @property
    def jsonSchema(self) -> dict[str : Any]:

        schema = super().jsonSchema
        schema["type"] = "integer"

        return schema



    def transformValueToPython(self, value: Any) -> Union[int, Any]:

        try: return int(value)
        except (ValueError, TypeError): return super().transformValueToPython(value)