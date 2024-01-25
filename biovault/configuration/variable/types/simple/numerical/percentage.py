from typing import Any

from biovault.configuration.variable.types.simple.numerical.float import Float

class Percentage(Float):


    def _completeVariableInfo(self,
                              variable: dict[str : Any],
                              widespread: dict[str : Any]) -> dict[str : Any]:


        variable = super()._completeVariableInfo(variable, widespread)

        if not "minimum" in variable["rules"]: variable["rules"]["minimum"] = 0.0
        if not "maximum" in variable["rules"]: variable["rules"]["maximum"] = 1.0

        return variable