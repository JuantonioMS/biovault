from typing import Any, Union
from datetime import date

class Variable:


    def __init__(self, variable: dict) -> None:

        self._variable = self._completeVariableInfo(variable)


    def _completeVariableInfo(self, variable: dict) -> dict:

        if not "info" in variable: variable["info"] = {}
        if not "rules" in variable: variable["rules"] = {}
        if not "controls" in variable: variable["controls"] = []

        # Por defecto, las variables no son obligatorias de aparecer en el registro
        if not "required" in variable["rules"]: variable["rules"]["required"] = False
        else: variable["rules"]["required"] = bool(variable["rules"]["required"])

        return variable



    def fabrica(self) -> Any:

        from biovault.configuration.variable.types.simple.numerical.integer import Integer
        from biovault.configuration.variable.types.simple.numerical.float import Float
        from biovault.configuration.variable.types.simple.numerical.date import Date
        from biovault.configuration.variable.types.simple.numerical.percentage import Percentage
        from biovault.configuration.variable.types.simple.categorical.ranking import Ranking
        from biovault.configuration.variable.types.simple.categorical.ordinal import Ordinal
        from biovault.configuration.variable.types.simple.categorical.nominal import Nominal
        from biovault.configuration.variable.types.simple.categorical.string import String
        from biovault.configuration.variable.types.simple.categorical.binomial import Binomial
        from biovault.configuration.variable.types.simple.categorical.boolean import Boolean
        from biovault.configuration.variable.types.complex.list import List
        from biovault.configuration.variable.types.complex.multilabel import Multilabel
        from biovault.configuration.variable.types.complex.object import Object

        return locals()[self.type.capitalize()](self._variable)



    def transformValueToPython(self,
                          value: Any) -> Any:
        return value



    def transformValueToJson(self,
                             value: Any) -> Union[str, bool, int, float, list, dict]:

        if isinstance(value, (str, bool, int, float, list, dict)): return value
        else: return str(value)



    @property
    def name(self) -> str:
        return self._variable["name"]


    @property
    def type(self) -> str:
        return self._variable["type"]


    @property
    def longName(self) -> str:
        try: return self._variable["info"]["longName"]
        except KeyError: return self.name


    @property
    def description(self) -> str:
        try: return self._variable["info"]["description"]
        except KeyError: return ""


    @property
    def groups(self) -> set:
        try: return self._variable["info"]["groups"]
        except KeyError: return set()


    @property
    def format(self) -> str:
        try: return self._variable["info"]["format"]
        except KeyError: return ""


    @property
    def rules(self) -> None:
        try: return Rules(self, self._variable["rules"])
        except KeyError: return Rules(self, {})


    @property
    def controls(self) -> None:
        try: return Controls(self, self._variable["controls"])
        except KeyError: return Controls(self, [])


    @property
    def jsonDumpFormat(self) -> dict:
        return self._variable


    @property
    def jsonSchema(self) -> dict:

        schema = {}
        for rule, value in self.jsonDumpFormat["rules"].items():

            if rule in ["required"]: continue

            schema[rule] = value

        return schema



class Rules:

    def __init__(self, variable: Any, rules: dict) -> None:
        self._rules = rules


class Controls:

    def __init__(self, variable: Any, controls: list) -> None:
        self._controls = controls