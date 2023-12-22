from biovault.configuration.variable.types.simple.numerical.float import Float

class Percentage(Float):


    def _completeVariableInfo(self, variable: dict) -> dict:

        variable = super()._completeVariableInfo(variable)

        variable["rules"]["minimum"] = 0.0
        variable["rules"]["maximum"] = 1.0

        return variable