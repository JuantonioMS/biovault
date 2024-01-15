from typing import Any

from biovault.configuration.variable.types.complex.list import List

class Multilabel(List):

    def transformValueToPython(self,
                               value: list[Any] | Any) -> list[Any] | Any:

        try:
            return [self._variable["rules"]["items"].transformValueToPython(element) for element in value.split(";")]

        except ValueError: return super().transformValueToPython(value)