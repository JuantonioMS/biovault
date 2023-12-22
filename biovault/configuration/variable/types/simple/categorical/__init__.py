from biovault.configuration.variable.types.simple import Simple

class Categorical(Simple):

    def _completeVariableInfo(self, variable: dict) -> dict:

        variable = super()._completeVariableInfo(variable)

        variable["rules"]["type"] = "string"

        if variable["type"] != "ranking" and "enum" in variable["rules"] and isinstance(variable["rules"]["enum"], str):
            variable["rules"]["enum"] = [element.strip(" ") for element in variable["rules"]["enum"].split(";")]

        return variable