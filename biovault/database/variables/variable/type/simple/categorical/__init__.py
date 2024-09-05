from typing import Any

from biovault.database.variables.variable.type.simple import Simple


class Categorical(Simple):


    @property
    def jsonSchema(self) -> dict:

        schema = super().jsonSchema
        schema["type"] = "string"
        return schema



    @classmethod
    def valueToPython(cls, value: Any) -> str:

        try:
            if value is None: return None
            return str(value).strip(" \n\t\r_-,./;+*")

        except ValueError: return super().valueToPython(value)




from biovault.database.variables.variable.type.simple.categorical.string import String
from biovault.database.variables.variable.type.simple.categorical.nominal import Nominal
from biovault.database.variables.variable.type.simple.categorical.binomial import Binomial
from biovault.database.variables.variable.type.simple.categorical.boolean import Boolean
from biovault.database.variables.variable.type.simple.categorical.ordinal import Ordinal
from biovault.database.variables.variable.type.simple.categorical.ranking import Ranking