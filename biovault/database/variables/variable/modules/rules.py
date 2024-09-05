from collections import UserDict
from typing import Any, ItemsView

from biovault.configuration.constants import RULES_DEFAULT_REQUIRED


class Rules(UserDict):


    def __init__(self, dict = None) -> None:

        super().__init__(dict)

        self._checkRequired()
        self._checkEnum()
        self._checkDates()

        self._checkItems()
        self._checkProperties()


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Checkers


    def _checkRequired(self) -> None:

        if "required" not in self:
            self["required"] = RULES_DEFAULT_REQUIRED



    def _checkEnum(self) -> None:
        if "enum" in self:
            if isinstance(self["enum"], str):
                self["enum"] = [element.strip() for element in self["enum"].split(";")]



    def _checkDates(self) -> None:

        from biovault.database.variables.variable.type.simple.numerical import Date

        for keyword in ["dateMinimum", "dateMaximum"]:
            if keyword in self:
                self[keyword] = Date.valueToPython(self[keyword])



    def _checkItems(self) -> None:

        from biovault.database.variables.variable import Variable

        if "items" in self:
            self["items"] = Variable(self["items"]).factory()



    def _checkProperties(self) -> None:

        from biovault.database.variables.variable import Variable

        if "properties" in self:

            properties = {}

            for property in self["properties"]:

                variable = Variable(property).factory()
                properties[variable.name] = variable

            self["properties"] = properties
            self["additionalProperties"] = False


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Properties


    @property
    def properties(self) -> dict:
        return self["properties"]



    @property
    def items(self) -> dict:
        return self["items"]



    @property
    def required(self) -> bool:
        return self["required"]


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region JSON schema


    @property
    def jsonSchema(self) -> dict[str, Any]:

        schema = {}
        for keyword, value in self.data.items():

            if keyword == "required": continue


            elif keyword in ["dateMinimum", "dateMaximum"]:

                from biovault.database.variables.variable.type.simple.numerical import Date

                schema[keyword] = Date.valueToJson(value)


            elif keyword == "items":

                schema[keyword] = value.jsonSchema


            elif keyword == "properties":

                schema[keyword] = {property.name: property.jsonSchema \
                                   for property in value.values()}

                schema["required"] = []
                for property in value.values():
                    if property.rules.required:
                        schema["required"].append(property.name)


            else: schema[keyword] = value

        return schema