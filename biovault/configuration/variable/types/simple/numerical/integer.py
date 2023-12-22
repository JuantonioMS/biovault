from biovault.configuration.variable.types.simple.numerical import Numerical

class Integer(Numerical):


    def _completeVariableInfo(self, variable: dict) -> dict:

        variable = super()._completeVariableInfo(variable)

        variable["rules"]["type"] = "integer"

        return variable