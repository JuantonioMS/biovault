from biovault.configuration.variable.types.simple import Simple

class Numerical(Simple):


    def _completeVariableInfo(self, variable: dict) -> dict:

        variable = super()._completeVariableInfo(variable)

        variable["rules"]["type"] = "number"

        return variable