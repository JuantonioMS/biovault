from typing import Any, Union, TypeVar
Register = TypeVar("Register")

DEFAULT_TYPE = "string"
DEFAULT_RULES_REQUIRED = False

class Variable:


    #%%  INITIALIZATION METHODS_________________________________________________________________________________________

    def __init__(self,
                 variable: dict[str : Any],
                 widespread: dict[str : Any] = {}) -> None:

        self._variable = self._completeVariableInfo(variable,
                                                    widespread)



    def _completeVariableInfo(self,
                              variable: dict[str : Any],
                              widespread: dict[str : Any]) -> dict[str : Any]:

        """
        Complete the variable info with the widespread info.

        Args:
            variable (dict)  : variable info.
            widespread (dict): widespread info.

        Returns:
            dict: completed variable info.
        """

        #  1. Assign name section
        #  TODO: Design a useful system to assign names by widespread

        #  2. Assign type section
        if not "type" in variable:
            if "type" in widespread: variable["type"] = widespread["type"] #  Spread type
            else: variable["type"] = DEFAULT_TYPE #  Type by default

        #  3. Assign info section
        if not "info" in variable: variable["info"] = {}

        if "info" in widespread and "groups" in widespread["info"]:
            try: #  Update variable info groups
                variable["info"]["groups"] = set(variable["info"]["groups"]) | set(widespread["info"]["groups"])
            except KeyError: #  Set widespread info groups as variable info groups
                variable["info"]["groups"] = widespread["info"]["groups"]

        #  4. Assign rules section
        if not "rules" in variable: variable["rules"] = {}

        if "rules" in widespread:
            for rule in widespread["rules"]:
                if rule not in variable["rules"]:
                    variable["rules"][rule] = widespread["rules"][rule]

        if not "required" in variable["rules"]:
            variable["rules"]["required"] = DEFAULT_RULES_REQUIRED

        #  5. Assign controls section
        if not "controls" in variable: variable["controls"] = []

        return variable



    def factory(self) -> Any:

        """
        Return the variable object instance with an especific variable type instance.
        It is a Factory Method Pattern Design.
        """

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



    #%%  GENERAL PROPERTIES METHODS_____________________________________________________________________________________

    @property
    def name(self) -> str:
        return self._variable["name"]



    @property
    def type(self) -> str:
        return self._variable["type"]



    #  GENERAL PROPERTIES INFO METHODS__________________________________________________________________________________

    @property
    def info(self) -> dict[str : Any]:
        return self._variable["info"]



    @property
    def longName(self) -> str:
        try: return self.info["longName"]
        except KeyError: return self.name



    @property
    def description(self) -> str:
        try: return self.info["description"]
        except KeyError: return ""



    @property
    def groups(self) -> set[str]:
        try: return self.info["groups"]
        except KeyError: return set()




    #  GENERAL PROPERTIES RULES METHODS_________________________________________________________________________________

    @property
    def rules(self) -> dict[str : Any]:
        return self._variable["rules"]



    #  GENERAL PROPERTIES CONTROLS METHODS______________________________________________________________________________

    @property
    def controls(self) -> list[dict]:
        return self._variable["rules"]



    #%%  TRANSFORM METHODS______________________________________________________________________________________________

    def transformValueToPython(self,
                               value: Any) -> Any:
        return value



    def transformValueToJson(self,
                             value: Any) -> Union[str, bool, int, float, list, dict]:

        if isinstance(value, (str, bool, int, float, list, dict)): return value
        else: return str(value)



    #%%  JSON METHODS___________________________________________________________________________________________________

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



    #%%  FORMULA METHODS________________________________________________________________________________________________

    def isFormula(self) -> bool:
        return "formula" in self.info



    @property
    def formula(self) -> str:

        if not self.isFormula(): return ""

        else:
            if isinstance(self.info["formula"], dict):
                return self.info["formula"]["formula"]

            else: return self.info["formula"]



    @property
    def imports(self) -> list[str]:

        try: return self._variable["info"]["imports"]
        except (KeyError, TypeError): return []



    def _applyFormula(self,
                     register: Register) -> Any:

        value = self._evalSentence(self.formula,
                                   imports = self.imports,
                                   register = register)

        return self.transformValueToPython(value)



    @staticmethod
    def _evalSentence(sentence: str,
                     imports: list[str] = [],
                     **kwargs) -> Any:

        for element in imports:
            exec(element)

        locals().update(kwargs)

        try: return eval(sentence)
        except (ValueError, TypeError, NameError, KeyError, IndexError): return None