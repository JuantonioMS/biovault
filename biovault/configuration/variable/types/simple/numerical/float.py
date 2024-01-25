from typing import Any, Union

from biovault.configuration.variable.types.simple.numerical import Numerical

class Float(Numerical):
    
    @property
    def jsonSchema(self) -> dict[str : Any]:

        schema = super().jsonSchema
        schema["type"] = "number"

        return schema

    def transformValueToPython(self, value: Any) -> Union[float, Any]:

        try: return float(value)
        except (ValueError, TypeError): return super().transformValueToPython(value)