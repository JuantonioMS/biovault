from typing import Any

from biovault.database.variables.variable.modules import Info, Formula, Rules, Controls
from biovault.configuration.constants import DEFAULT_VALUE_GENERAL, DEFAULT_VARIABLE_TYPE
from biovault import utils


class Variable:


    DEFAULT_VALUE = DEFAULT_VALUE_GENERAL


    def __init__(self,
                 variable: dict[str : Any] = {},
                 widespread: dict[str : Any] = {}) -> None:

        #  1. Assign name section

        try: self.name = variable["name"]
        except KeyError: raise NameError("Name field is required in variable section")

        #  2. Assign type section

        if "type" in variable: self.type = variable["type"]
        elif "type" in widespread: self.type = widespread["type"]
        else: self.type = DEFAULT_VARIABLE_TYPE

        #  3. Assign info section

        if not "info" in variable: variable["info"] = {"groups": set(), "longName": self.name}
        if not "groups" in variable["info"]: variable["info"]["groups"] = set()
        if not "longName" in variable["info"]: variable["info"]["longName"] = self.name

        if "info" in widespread and "groups" in widespread["info"]:
            variable["info"]["groups"] = set(variable["info"]["groups"]) | set(widespread["info"]["groups"])

        self.info = Info(**variable["info"])

        #  4. Assign formula section

        if "formula" in variable and isinstance(variable["formula"], str):
            self.formula = Formula(variable["formula"])
        elif "formula" in variable and "imports" in variable["formula"]:
            self.formula = Formula(variable["formula"]["sentence"], variable["formula"]["imports"])
        elif "formula" in variable:
            self.formula = Formula(variable["formula"]["sentence"])
        else:
            self.formula = Formula()

        #  5. Assign rules section

        if not "rules" in variable: variable["rules"] = {}
        if not "rules" in widespread: widespread["rules"] = {}
        self.rules = Rules(widespread["rules"] | variable["rules"])

        #  6. Assign controls section

        if not "controls" in variable: variable["controls"] = []
        self.controls = Controls(variable["controls"])




    def factory(self) -> Any:

        from biovault.database.variables.variable.type.simple.numerical import Integer, Float, Percentage, Date
        from biovault.database.variables.variable.type.simple.categorical import String, Nominal, Binomial, Boolean, Ordinal, Ranking
        from biovault.database.variables.variable.type.complex import List, Object, Multilabel, Multivalue

        return locals()[self.type.capitalize()](self)


#%%  TRANSFORM METHODS__________________________________________________________________________________________________


    @classmethod
    def transformValueToPython(cls, value: Any) -> Any:
        return value




    @classmethod
    def transformValueToJson(cls, value: Any) -> str | bool | int | float | list | dict:
        if isinstance(value, (str, bool, int, float, list, dict)): return value
        else: return str(value)


#%%  JSON SCHEMA METHODS________________________________________________________________________________________________


    @property
    def jsonSchema(self) -> dict[str, Any]: return self.rules.jsonSchema

    def isFormula(self) -> bool: return bool(self.formula)




    def isAlreadyCalculated(self, content: Any) -> bool:

        if not self.isFormula(): return True
        else: return content != self.DEFAULT_VALUE




    def _applyFormula(self, content: Any, **kwargs) -> Any:

        value = utils.evalSentence(self.formula.sentence,
                                   imports = self.formula.imports,
                                   **kwargs)

        return self.transformValueToPython(value)