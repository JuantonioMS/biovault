from typing import Any

from biovault.database.variables.variable.type.simple.categorical import Binomial


class Boolean(Binomial):


    @property
    def jsonSchema(self) -> dict:

        schema = super().jsonSchema
        schema["type"] = "boolean"
        return schema



    @classmethod
    def valueToPython(cls, value: Any) -> bool:

        try:

            if isinstance(value, bool): return value

            elif isinstance(value, (int, float)) and value in [0, 1]: return bool(value)

            elif isinstance(value, str):

                if value.lower() in ["si", "sí", "yes", "s", "y", "t", "true", "1"]: return True
                elif value.lower() in ["no", "n", "f", "false", "0"]: return False
                else: return value

            else: return value

        except ValueError: return super().valueToPython(value)