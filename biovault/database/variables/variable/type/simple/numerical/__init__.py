from biovault.database.variables.variable.type.simple import Simple


class Numerical(Simple):

    @property
    def jsonSchema(self) -> dict:

        schema = super().jsonSchema
        schema["type"] = self.type if self.type not in ["float", "percentage"] else "number"
        return schema



from biovault.database.variables.variable.type.simple.numerical.float import Float
from biovault.database.variables.variable.type.simple.numerical.integer import Integer
from biovault.database.variables.variable.type.simple.numerical.percentage import Percentage
from biovault.database.variables.variable.type.simple.numerical.date import Date