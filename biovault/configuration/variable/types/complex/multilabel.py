from typing import Any

from biovault.configuration.variable.types.complex.list import List

class Multilabel(List):

    def transformValueToPython(self,
                               value: list[Any] | Any) -> list[Any] | Any:

        try:
            if isinstance(value, str):
                return [self._variable["rules"]["items"].transformValueToPython(element) for element in value.split(";")]
            else:
                return [str(element) for element in value]

        except ValueError: return super().transformValueToPython(value)