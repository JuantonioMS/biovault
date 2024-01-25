from typing import Any
from biovault.configuration.variable.types.simple.categorical import Categorical

class Nominal(Categorical):


    def _completeVariableInfo(self,
                              variable: dict[str : Any],
                              widespread: dict[str : Any]) -> dict[str : Any]:

        variable = super()._completeVariableInfo(variable, widespread)

        if "enum" in variable["rules"] and isinstance(variable["rules"]["enum"], str):
            variable["rules"]["enum"] = ";".split(variable["rules"]["enum"])

        return variable