from typing import Any
from biovault.configuration.variable.types.complex import Complex

class Object(Complex):


    def _completeVariableInfo(self,
                              variable: dict[str : Any],
                              widespread: dict[str : Any]) -> dict[str : Any]:

        variable = super()._completeVariableInfo(variable, widespread)

        from biovault.configuration.variable import Variable

        properties = {}
        for property in variable["rules"]["properties"]:
            properties[property["name"]] = Variable(property).factory()

        variable["rules"]["properties"] = properties

        return variable



    @property
    def jsonSchema(self) -> dict[str, Any]:

        schema = super().jsonSchema

        schema["type"] = "object"
        schema["additionalProperties"] = False

        required = []
        for property in self.properties.values():

            schema["properties"][property.name] = property.jsonSchema

            try:
                if property.jsonSchema["required"]: required.append(property.name)
            except KeyError: pass

        schema["required"] = required

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