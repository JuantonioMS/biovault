from typing import Any, Union

from biovault.database.variables.variable.type.simple.numerical import Numerical

class Integer(Numerical):


    @classmethod
    def valueToPython(cls, value: Any) -> int:

        try: return int(value)
        except (ValueError, TypeError): return super().valueToPython(value)