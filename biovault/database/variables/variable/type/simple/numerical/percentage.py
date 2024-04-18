from typing import Any

from biovault.database.variables.variable.type.simple.numerical import Float


class Percentage(Float):


    def __init__(self, object) -> None:

        super().__init__(object)

        if not "minimum" in self.rules: self.rules["minimum"] = 0.0
        if not "maximum" in self.rules: self.rules["maximum"] = 1.0