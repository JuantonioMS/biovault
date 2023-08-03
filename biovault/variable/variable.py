import pandas as pd
from typing import Any


class Variable:


    def __init__(self, info: dict) -> None:
        self.info = info


    #  PROPERTIES_______________________________________________________________________________________________________


    #      description--------------------------------------------------------------------------------------------------


    @property
    def type(self) -> str: return self.info["description"]["type"]

    @property
    def name(self) -> str: return self.info["description"]["name"]


    #      info---------------------------------------------------------------------------------------------------------


    @property
    def longName(self) -> str:
        try: return self.info["info"]["longName"]
        except KeyError: return self.name

    @property
    def groups(self) -> set:
        try: return set(self.info["info"]["groups"])
        except KeyError: return set()


    #      rules & controls---------------------------------------------------------------------------------------------


    @property
    def mandatory(self) -> bool:

        try: return self.info["rules"]["mandatory"]
        except KeyError: return False


    @property
    def controls(self) -> list:
        try: return self.info["controls"]
        except KeyError: return []


    #      source-------------------------------------------------------------------------------------------------------


    @property
    def sourceFile(self) -> str:
        return self.info["source"]["file"]

    @property
    def sourceSheet(self) -> str:
        try: return self.info["source"]["sheet"]
        except KeyError: return ""

    @property
    def sourceName(self) -> str:
        try: return self.info["source"]["name"]
        except KeyError: return ""

    @property
    def sourceFormat(self) -> str:
        try: return self.info["source"]["format"]
        except KeyError: return ""


    #  CHECKS___________________________________________________________________________________________________________


    def checkValue(self, value: Any, **kwargs) -> list:
        return not any([not value for value in self._checkRules(value) + self._checkControls(value, **kwargs)])



    def _checkRules(self, value: Any) -> list:

        if self.mandatory:
            return [value is not None]

        else: return [True]



    def _checkControls(self, value: Any) -> list:

        checks = []
        for control in self.controls:
            pass

        return checks


    #  METHODS__________________________________________________________________________________________________________


    def _extractData(self,
                     databases: dict,
                     columnIdName: str,
                     registers: object) -> object:

        from biovault.register import Register

        dataframe = pd.read_excel(databases[self.sourceFile],
                                  sheet_name = self.sourceSheet)

        dataframe = self._reduceDataframe(dataframe,
                                          columnIdName)

        for _, row in dataframe.iterrows():

            id, value = self._splitIdAndValue(row, columnIdName)
            value = self._transformValue(value)

            if not id in registers:
                registers.addRegister(Register(id = id))

            registers[id].addData(self.name, value)

        return registers



    def _reduceDataframe(self,
                         dataframe: pd.DataFrame,
                         columnIdName: str) -> pd.DataFrame:

        return dataframe[[columnIdName, self.sourceName]]



    def _splitIdAndValue(self,
                         row: pd.Series,
                         columnIdName: str) -> tuple:

        return row[columnIdName], row[self.sourceName]



    def _transformValue(self,
                        value: Any) -> Any:

        return value


    #  RELOAD VARIABLE__________________________________________________________________________________________________


    def getSpecificVariable(self):

        from biovault.variable.type import Integer, Float, \
                                           String, Nominal, Multilabel, Ordinal, Binomial, Boolean, \
                                           Date, Object, Listed

        try: return locals()[self.type.capitalize()](self.info)
        except NameError: return self