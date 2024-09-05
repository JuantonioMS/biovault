import pandas as pd
from typing import Any

from biovault.database.variables.variable.modules import Info, Formula, Rules, Controls
from biovault.configuration.constants import DEFAULT_VALUE_GENERAL, DEFAULT_VARIABLE_TYPE
from biovault import utils


class Variable:


    DEFAULT_VALUE = DEFAULT_VALUE_GENERAL


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Initialization


    def __init__(self,
                 variable: dict[str : Any] = {},
                 widespread: dict[str : Any] = {}) -> None:

        self.__init__name(variable, widespread)     #  1. Assign name section
        self.__init__type(variable, widespread)     #  2. Assign type section
        self.__init__info(variable, widespread)     #  3. Assign info section
        self.__init__formula(variable, widespread)  #  4. Assign formula section
        self.__init__rules(variable, widespread)    #  5. Assign rules section
        self.__init__controls(variable, widespread) #  6. Assign controls section




    def __init__name(self, variable: dict, widespread: dict) -> None:

        try: self.name = variable["name"]
        except KeyError: raise NameError("Name field is required in variable section")




    def __init__type(self, variable: dict, widespread: dict) -> None:

        if "type" in variable: self.type = variable["type"]
        elif "type" in widespread: self.type = widespread["type"]
        else: self.type = DEFAULT_VARIABLE_TYPE




    def __init__info(self, variable: dict, widespread: dict) -> None:

        if not "info" in variable: variable["info"] = {"groups": set(), "longName": self.name}
        if not "groups" in variable["info"]: variable["info"]["groups"] = set()
        else: variable["info"]["groups"] = set(variable["info"]["groups"])
        if "info" in widespread and "groups" in widespread["info"]: variable["info"]["groups"] |= set(widespread["info"]["groups"])
        if not "longName" in variable["info"]: variable["info"]["longName"] = self.name
        self.info = Info(**variable["info"])




    def __init__formula(self, variable: dict, widespread: dict) -> None:

        if "formula" in variable and isinstance(variable["formula"], str): self.formula = Formula(variable["formula"])
        elif "formula" in variable and "imports" in variable["formula"]: self.formula = Formula(variable["formula"]["sentence"], variable["formula"]["imports"])
        elif "formula" in variable: self.formula = Formula(variable["formula"]["sentence"])
        else: self.formula = Formula()




    def __init__rules(self, variable: dict, widespread: dict) -> None:

        if not "rules" in variable: variable["rules"] = {}
        if not "rules" in widespread: widespread["rules"] = {}
        self.rules = Rules(widespread["rules"] | variable["rules"])




    def __init__controls(self, variable: dict, widespread: dict) -> None:

        if not "controls" in variable: variable["controls"] = []
        self.controls = Controls(*variable["controls"])




    def factory(self) -> Any:

        from biovault.database.variables.variable.type.simple.numerical import Integer, Float, Percentage, Date
        from biovault.database.variables.variable.type.simple.categorical import String, Nominal, Binomial, Boolean, Ordinal, Ranking
        from biovault.database.variables.variable.type.complex import List, Object, Multilabel, Multivalue

        return locals()[self.type.capitalize()](self)


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Converters


    @classmethod
    def valueToPython(cls, value: Any) -> Any:
        return value




    @classmethod
    def valueToJson(cls, value: Any) -> str | bool | int | float | list | dict:
        if isinstance(value, (str, bool, int, float, list, dict)): return value
        else: return str(value)


#%%  JSON SCHEMA METHODS________________________________________________________________________________________________

#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region JSON schema


    @property
    def jsonSchema(self) -> dict[str, Any]:
        return self.rules.jsonSchema


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Formula


    def isFormula(self) -> bool:
        return bool(self.formula)




    def isAlreadyCalculated(self, content: Any) -> bool:

        if not self.isFormula(): return True
        else: return content != self.DEFAULT_VALUE




    def _applyFormula(self, content: Any, **kwargs) -> Any:

        value = utils.evalSentence(self.formula.sentence,
                                   imports = self.formula.imports,
                                   **kwargs)

        return self.valueToPython(value)


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Dataframe


    def toDataframe(self, registers) -> pd.DataFrame:

        return pd.DataFrame(data = [register[self.name] for register in registers],
                            index = [register.id for register in registers],
                            columns = [self.name])


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Properties


    @property
    def groups(self) -> set:
        return self.info.groups