from typing import Any, Union

from biovault.configuration.variable.types.simple.numerical import Numerical

class Float(Numerical):

    def transformValueToPython(self, value: Any) -> Union[float, Any]:

        try: return float(value)
        except ValueError: return value