from typing import Any
import pandas as pd

from biovault import Variable
from biovault.variable.type import Complex


class Listed(Complex):


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