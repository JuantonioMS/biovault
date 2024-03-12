from typing import Any

from biovault.configuration.variable.types.complex import Complex

class List(Complex):


    def _completeVariableInfo(self,
                              variable: dict[str : Any],
                              widespread: dict[str : Any]) -> dict[str : Any]:

        variable = super()._completeVariableInfo(variable, widespread)

        from biovault.configuration.variable import Variable

        variable["rules"]["items"] = Variable(variable["rules"]["items"]).factory()

        return variable



    @property
    def nonDefinedValue(self) -> list:
        return []



    @property
    def jsonSchema(self) -> dict[str : Any]:

        schema = super().jsonSchema

        schema["type"] = "array"

        schema["items"] = self.items.jsonSchema

        return schema



    def transformValueToPython(self,
                               value: list[Any] | Any) -> list[Any] | Any:

        try:
            if isinstance(value, list):

                newValue = []
                for element in value:
                    if isinstance(element, dict):
                        newValue.append(self._variable["rules"]["items"].transformValueToPython(element))
                    else:
                        newValue.append(self._variable["rules"]["items"].transformValueToPython(element))

                return newValue

            else:
                if value is None: return None
                else: return [self._variable["rules"]["items"].transformValueToPython(value)]

        except ValueError: return value



    def transformValueToJson(self,
                             value: list[Any] | Any) -> list[Any] | Any:


        if isinstance(value, list):

            newValue = []
            for element in value:
                newValue.append(self._variable["rules"]["items"].transformValueToJson(element))

            return newValue

        else: return super().transformValueToJson(value)



    @property
    def items(self) -> Any:
        return self._variable["rules"]["items"]


    def isNestedFormula(self) -> bool:
        return self._variable["rules"]["items"].isFormula()



    def _applyFormula(self, register, object = None) -> Any:

        if self.isNestedFormula():
            aux = []

            if object is None: object = register[self.name]

            for element in object if not object is None else []:

                #if object is None: object = element

                value = self.items._applyFormula(register, object = element)
                aux.append(element | value)

            return aux

        else:
            return super()._applyFormula(register)