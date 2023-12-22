from biovault.configuration.variable.types.simple.categorical.binomial import Binomial

class Boolean(Binomial):


    def _completeVariableInfo(self, variable: dict) -> dict:

        variable = super()._completeVariableInfo(variable)

        variable["rules"]["type"] = "boolean"
        variable["rules"]["enum"] = [True, False]

        return variable