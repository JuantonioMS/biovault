from typing import Any

from biovault.variable.type import Number


class Integer(Number):


    def _transformValue(self, value: Any) -> int:
        return int(value)