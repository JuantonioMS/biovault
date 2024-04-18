from typing import Any

from biovault.database.variables.variable.type.complex import List


class Multivalue(List):


    def transformValueToPython(self, value: Any) -> list:

        try:
            if isinstance(value, str):
                return [self.rules.items.transformValueToPython(element) for element in value.split(";")]
            else:
                return [str(element) for element in value]

        except ValueError: return super().transformValueToPython(value)