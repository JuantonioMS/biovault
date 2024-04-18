from typing import Any

from biovault.database.variables.variable.type.complex import Complex
from biovault.configuration.constants import DEFAULT_VALUE_LIST


class List(Complex):

    DEFAULT_VALUE = DEFAULT_VALUE_LIST


    @property
    def jsonSchema(self) -> dict[str : Any]:

        schema = super().jsonSchema

        schema["type"] = "array"

        return schema



    def transformValueToPython(self,
                               value: list[Any] | Any) -> list[Any] | Any:

        try:
            if isinstance(value, list):

                newValue = []
                for element in value:
                    if isinstance(element, dict):
                        newValue.append(self.rules.items.transformValueToPython(element))
                    else:
                        newValue.append(self.rules.items.transformValueToPython(element))

                return newValue

            else:
                if value is None: return None
                else: return [self.rules.items.transformValueToPython(value)]

        except ValueError: return value



    def transformValueToJson(self,
                             value: list[Any] | Any) -> list[Any] | Any:


        if isinstance(value, list):

            newValue = []
            for element in value:
                newValue.append(self.rules.items.transformValueToJson(element))

            return newValue

        else: return super().transformValueToJson(value)




    def isNestedFormula(self) -> bool:
        return self.rules.items.isFormula()



    def _applyFormula(self, content: list, **kwargs) -> Any:

        if not self.isNestedFormula():
            return super()._applyFormula(content, **kwargs)

        else:

            values = []
            for element in content:

                values.append(self.rules.items._applyFormula(element, **kwargs | {"own" : element}))

            return values



    def isAlreadyCalculated(self, content: Any) -> bool:

        if not self.isFormula(): return True

        if content == self.DEFAULT_VALUE:
            return False

        else:

            for element in content:
                if self.rules.items.isAlreadyCalculated(element) == False:
                    return False

        return True