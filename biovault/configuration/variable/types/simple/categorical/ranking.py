from biovault.configuration.variable.types.simple.categorical.ordinal import Ordinal

class Ranking(Ordinal):


    def _completeVariableInfo(self, variable: dict) -> dict:

        variable = super()._completeVariableInfo(variable)

        variable["rules"]["type"] = "number"

        if "enum" in variable["rules"]:
            minimum, maximum = variable["rules"]["enum"].split(":")
            variable["rules"]["minimum"] = int(minimum[1:])
            variable["rules"]["maximum"] = int(maximum[:-1])

            del variable["rules"]["enum"]

        return variable