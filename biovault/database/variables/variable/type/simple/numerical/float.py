from typing import Any

from biovault.database.variables.variable.type.simple.numerical import Numerical


class Float(Numerical):


    @classmethod
    def valueToPython(cls, value: Any) -> float:

        try: return float(value)
        except (ValueError, TypeError): return super().valueToPython(value)