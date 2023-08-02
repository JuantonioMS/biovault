from typing import Any

from biovault.variable import Variable


class Float(Variable):


    def _transformValue(self, value: Any) -> float:
        return float(value)