from typing import Any, Union

from biovault.configuration.variable.types.simple.numerical import Numerical

class Integer(Numerical):


    def _completeVariableInfo(self, variable: dict) -> dict:

        variable = super()._completeVariableInfo(variable)

        variable["rules"]["type"] = "integer"

        return variable



    def transformValueToPython(self, value: Any) -> Union[int, Any]:

        try: return int(value)
        except ValueError: return value