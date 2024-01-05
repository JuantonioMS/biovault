from copy import deepcopy
from datetime import date
import pandas as pd

from biovault.configuration.variable.types.simple.numerical import Numerical

class Date(Numerical):


    def _completeVariableInfo(self, variable: dict) -> dict:

        variable = super()._completeVariableInfo(variable)

        variable["rules"]["type"] = "string"
        variable["rules"]["format"] = "date"

        for edge in ["formatMinimum", "formatMaximum"]:

            if edge in variable["rules"]:
                if isinstance(variable["rules"][edge], str):
                    variable["rules"][edge] = date.fromisoformat(variable["rules"][edge])
                elif isinstance(variable["rules"][edge], pd._libs.tslibs.timestamps.Timestamp):
                    variable["rules"][edge] = variable["rules"][edge].to_pydatetime().date()

        return variable


    @property
    def jsonDumpFormat(self) -> dict:
        aux = deepcopy(super().jsonDumpFormat)

        for edge in ["formatMinimum", "formatMaximum"]:
            if edge in aux["rules"]:
                aux["rules"][edge] = aux["rules"][edge].strftime("%Y-%m-%d")

        return aux