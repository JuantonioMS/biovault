from typing import Any, Union

from biovault.configuration.variable.types.simple.categorical.binomial import Binomial

class Boolean(Binomial):


    def _completeVariableInfo(self, variable: dict) -> dict:

        variable = super()._completeVariableInfo(variable)

        variable["rules"]["type"] = "boolean"
        variable["rules"]["enum"] = [True, False]

        return variable



    def transformValueToPython(self, value: Any) -> Union[bool, Any]:

        try:

            if isinstance(value, bool): return value

            elif isinstance(value, (int, float)): return bool(value)

            elif isinstance(value, str):

                if value.lower() in ["si", "sí", "yes", "s", "y", "t", "true", "1"]: return True
                elif value.lower() in ["no", "n", "f", "false", "0"]: return False
                else: return value

            else: return value

        except ValueError: return value