from typing import Any

from biovault.variable import Variable


class Integer(Variable):


    def _transformValue(self, value: Any) -> int:
        return int(value)