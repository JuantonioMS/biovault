from datetime import date, datetime
import pandas as pd
from typing import Any, Union

from biovault.database.variables.variable.type.simple.numerical import Numerical


class Date(Numerical):


    @classmethod
    def valueToPython(cls, value: Any) -> date:

        try:
            if isinstance(value, str): return date.fromisoformat(value)
            elif isinstance(value, pd._libs.tslibs.timestamps.Timestamp): return value.to_pydatetime().date()
            elif isinstance(value, datetime): return value.date()
            else: return value

        except ValueError: return super().valueToPython(value)



    @classmethod
    def valueToJson(cls, value: Any) -> str:

        if isinstance(value, date): return value.isoformat()
        else: return super().valueToJson(value)