from typing import Any, Union

from biovault.configuration.variable.types.simple.categorical.ordinal import Ordinal

class Ranking(Ordinal):

    @property
    def jsonSchema(self) -> dict[str : Any]:

            schema = super().jsonSchema
            schema["type"] = "integer"

            return schema


    def _completeVariableInfo(self,
                              variable: dict[str : Any],
                              widespread: dict[str : Any]) -> dict[str : Any]:

        variable = super()._completeVariableInfo(variable, widespread)

        if "enum" in variable["rules"]:
            minimum, maximum = variable["rules"]["enum"].split(":")
            variable["rules"]["minimum"] = int(minimum[1:])
            variable["rules"]["maximum"] = int(maximum[:-1])

            del variable["rules"]["enum"]

        return variable



    def transformValueToPython(self, value: Any) -> Union[int, Any]:

        try: return int(value)
        except ValueError: return super().transformValueToPython(value)