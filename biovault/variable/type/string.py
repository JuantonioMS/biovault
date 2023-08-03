from typing import Any

from biovault.variable import Variable


class String(Variable):


    def _transformValue(self, value: Any) -> str:
        return str(value).lstrip(" ").rstrip(" ")