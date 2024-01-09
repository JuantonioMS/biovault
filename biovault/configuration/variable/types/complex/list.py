from typing import Any

from biovault.configuration.variable.types.complex import Complex

class List(Complex):


    def _completeVariableInfo(self,
                              variable: dict) -> dict:

        from biovault.configuration.variable import Variable

        variable = super()._completeVariableInfo(variable)

        variable["rules"]["items"] = Variable(variable["rules"]["items"]).fabrica()

        return variable



    @property
    def jsonSchema(self) -> dict[str : Any]:

        schema = {"type" : "array"}
        for rule, value in self.jsonDumpFormat["rules"].items():

            if rule in ["required"]: continue

            if rule == "items":


                schema[rule] = self._variable["rules"]["items"].jsonSchema
                continue

            schema[rule] = value

        return schema



    def transformValueToPython(self,
                               value: list[Any] | Any) -> list[Any] | Any:

        try:
            if isinstance(value, list):

                newValue = []
                for element in value:
                    newValue.append(self._variable["rules"]["items"].transformValueToPython(element))

                return newValue

            else:
                return [self._variable["rules"]["items"].transformValueToPython(value)]

        except ValueError: return value



    def transformValueToJson(self,
                             value: list[Any] | Any) -> list[Any] | Any:


        if isinstance(value, list):

            newValue = []
            for element in value:
                newValue.append(self._variable["rules"]["items"].transformValueToJson(element))

            return newValue

        else: return super().transformValueToJson(value)