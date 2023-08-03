from typing import Any

from biovault.variable.type import Number


class Float(Number):


    def _transformValue(self, value: Any) -> float:
        return float(value)