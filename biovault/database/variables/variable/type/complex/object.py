from copy import deepcopy
from typing import Any

from biovault.database.variables.variable.type.complex import Complex
from biovault.configuration.constants import DEFAULT_VALUE_OBJECT


class Object(Complex):

    DEFAULT_VALUE = DEFAULT_VALUE_OBJECT


    @property
    def jsonSchema(self) -> dict[str, Any]:

        schema = super().jsonSchema

        schema["type"] = "object"

        return schema




    def transformValueToPython(self,
                               value: dict[str, Any] | Any) -> dict[str, Any] | Any:

        try:
            if isinstance(value, dict):

                newValue = {}
                for name, value in value.items():
                    newValue[name] = self.rules.properties[name].transformValueToPython(value)

                return newValue

            else: return value

        except ValueError: return value



    def transformValueToJson(self,
                             value: dict[str, Any] | Any) -> dict[str, Any] | Any:

        if isinstance(value, dict):

            newValue = {}
            for name, value in value.items():
                newValue[name] = self.rules.properties[name].transformValueToJson(value)

            return newValue

        else: return super().transformValueToJson(value)




    def isNestedFormula(self) -> bool:
        return any([element.isFormula() for element in self.rules.properties.values()])




    def _applyFormula(self, content: dict, **kwargs) -> Any:

        if not self.isNestedFormula():
            return super()._applyFormula(content, **kwargs)

        else:

            values = {}
            for property in self.rules.properties.values():

                if property.name in content and \
                   property.isAlreadyCalculated(content[property.name]):

                       values[property.name] = property.transformValueToPython(content[property.name])

                else:
                    if not property.isFormula(): continue

                    if property.type in ["object", "list"] and property.isNestedFormula():

                        value = property._applyFormula(content[property.name] \
                                                       if property.name in content \
                                                       else property.DEFAULT_VALUE,
                                                       **kwargs | {"own" : content[property.name] \
                                                                           if property.name in content \
                                                                           else property.DEFAULT_VALUE})

                    else:

                        value = property._applyFormula(content[property.name] \
                                                       if property.name in content \
                                                       else property.DEFAULT_VALUE,
                                                       **kwargs)

                    values[property.name] = property.transformValueToPython(value)

            return values



    def isAlreadyCalculated(self, content: Any) -> bool:

        if not self.isFormula(): return True

        if content == self.DEFAULT_VALUE:
            return False

        else:

            for property in self.rules.properties.values():
                if property.name not in content: return False
                if property.isAlreadyCalculated(content[property.name]) == False: return False

        return True