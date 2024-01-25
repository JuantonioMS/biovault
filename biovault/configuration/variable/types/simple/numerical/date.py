from copy import deepcopy
from datetime import date, datetime
import pandas as pd
from typing import Any, Union

from biovault.configuration.variable.types.simple.numerical import Numerical

class Date(Numerical):


    @property
    def jsonSchema(self) -> dict[str : Any]:

        schema = super().jsonSchema
        schema["type"] = "date"

        return schema



    def _completeVariableInfo(self,
                              variable: dict[str : Any],
                              widespread: dict[str : Any]) -> dict[str : Any]:

        variable = super()._completeVariableInfo(variable, widespread)

        for edge in ["dateMinimum", "dateMaximum"]:
            if edge in variable["rules"]:
                variable["rules"][edge] = self.transformValueToPython(variable["rules"][edge])

        return variable



    @property
    def jsonDumpFormat(self) -> dict:
        aux = deepcopy(super().jsonDumpFormat)

        for edge in ["dateMinimum", "dateMaximum"]:
            if edge in aux["rules"]:
                aux["rules"][edge] = aux["rules"][edge].strftime("%Y-%m-%d")

        return aux



    def transformValueToPython(self,
                               value: Any) -> Union[date, Any]:

        try:

            if isinstance(value, str): return date.fromisoformat(value)
            elif isinstance(value, pd._libs.tslibs.timestamps.Timestamp): return value.to_pydatetime().date()
            elif isinstance(value, datetime): return value.date()
            else: return value

        except ValueError: return value



    def transformValueToJson(self,
                             value: Any) -> str:

        if isinstance(value, date): return value.isoformat()
        else: return super().transformValueToJson(value)