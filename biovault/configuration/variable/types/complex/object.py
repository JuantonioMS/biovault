from typing import Any
from biovault.configuration.variable.types.complex import Complex

class Object(Complex):


    def _completeVariableInfo(self,
                              variable: dict) -> dict:

        from biovault.configuration.variable import Variable

        variable = super()._completeVariableInfo(variable)

        aux = {}
        for property in variable["rules"]["properties"]:
            aux[property["name"]] = Variable(property).fabrica()

        variable["rules"]["properties"] = aux

        return variable



    @property
    def jsonSchema(self) -> dict[str, Any]:

        schema = {"type" : "object",
                  "additionalProperties": False}

        for rule, value in self.jsonDumpFormat["rules"].items():

            if rule in ["required"]: continue

            if rule == "properties":

                aux = {}
                for property in self.properties.values():
                    aux[property.name] = property.jsonSchema

                schema[rule] = aux
                continue

            schema[rule] = value

        schema["required"] = [property.name for property in self.properties.values() if property.jsonDumpFormat["rules"]["required"]]

        return schema



    def transformValueToPython(self,
                               value: dict[str, Any] | Any) -> dict[str, Any] | Any:

        try:
            if isinstance(value, dict):

                newValue = {}
                for name, value in value.items():
                    newValue[name] = self.properties[name].transformValueToPython(value)

                return newValue

            else: return value

        except ValueError: return value



    def transformValueToJson(self,
                             value: dict[str, Any] | Any) -> dict[str, Any] | Any:


        if isinstance(value, dict):

            newValue = {}
            for name, value in value.items():
                newValue[name] = self.properties[name].transformValueToJson(value)

            return newValue

        else: return super().transformValueToJson(value)



    @property
    def properties(self) -> dict[str : Any]:
        try: return self._variable["rules"]["properties"]
        except KeyError: return {}



    def isNestedFormula(self) -> bool:
        return any([element.isFormula() for element in self.properties.values()])



    def _applyFormula(self, register, object = None) -> Any:

        if self.isNestedFormula():

            buffer = {property.name : False for property in self.properties.values() if property.isFormula()}
            results = {}

            lengthStart, lengthEnd = 0, -1

            while lengthStart != lengthEnd:
                lengthStart = len(results)

                object = object if not object is None else register[self.name]
                if object is None: return None

                own = object | results

                for propertyName in buffer:

                    if not buffer[propertyName]:
                        property = self.properties[propertyName]

                        value = self._evalSentence(property.formula,
                                                   imports = property.imports,
                                                   register = register,
                                                   own = own)

                        if not value is None: results[property.name] = property.transformValueToPython(value)

                lengthEnd = len(results)

            return results

        else:
            return super()._applyFormula(register)