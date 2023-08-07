from typing import Any
import pandas as pd

from biovault import Variable
from biovault.variable.type import Complex


class Listed(Complex):


    def _checkRules(self, value: Any) -> list:

        checks = super()._checkRules(value)

        checks["items"] = []

        for element in value:
            checks["items"].append(self.item._checkRules(element))

        return checks



    def _checkControls(self, value: Any, **kwargs) -> list:

        controls = super()._checkControls(value)

        controls["items"] = []

        for element in value:
            controls["items"].append(self.item._checkControls(element, **kwargs))

        return controls


    @property
    def item(self) -> object:
        return Variable(self.info["item"]).getSpecificVariable()



    def _reduceDataframe(self,
                         dataframe: pd.DataFrame,
                         columnIdName: str) -> pd.DataFrame:

        return self.item._reduceDataframe(dataframe, columnIdName)



    def _splitIdAndValue(self,
                         row: pd.Series,
                         columnIdName: str) -> tuple:

        return self.item._splitIdAndValue(row, columnIdName)



    def _transformValue(self,
                        value: Any) -> dict:

        return [self.item._transformValue(value)]