from typing import Any, Union

from biovault.configuration.variable.types.simple import Simple

class Categorical(Simple):


    @property
    def jsonSchema(self) -> dict[str : Any]:

            schema = super().jsonSchema
            schema["type"] = "string"

            return schema



    def transformValueToPython(self, value: Any) -> Union[str, Any]:

        try: return str(value).strip(" \n\t\r_-,./;+*")
        except ValueError: return super().transformValueToPython(value)