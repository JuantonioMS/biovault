import pandas as pd
from typing import Any

from pandas.core.api import DataFrame as DataFrame

from biovault.database.variables.variable.type.complex import Complex
from biovault.configuration.constants import DEFAULT_VALUE_OBJECT


class Object(Complex):


    DEFAULT_VALUE = DEFAULT_VALUE_OBJECT


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region JSON schema


    @property
    def jsonSchema(self) -> dict:

        schema = super().jsonSchema
        schema["type"] = "object"
        return schema


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Converters


    def valueToPython(self, value: Any) -> dict:

        try:
            if isinstance(value, dict):

                newValue = {}
                for name, value in value.items():
                    newValue[name] = self.rules.properties[name].valueToPython(value)

                return newValue

            else: return value

        except ValueError: return value



    def valueToJson(self, value: Any) -> dict:

        if isinstance(value, dict):

            newValue = {}
            for name, value in value.items():
                newValue[name] = self.rules.properties[name].valueToJson(value)

            return newValue

        else: return super().valueToJson(value)


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Formula


    def isNestedFormula(self) -> bool:
        return any([property.isFormula() for property in self.rules.properties.values()])



    def _applyFormula(self, content: dict, **kwargs) -> Any:

        if not self.isNestedFormula():
            return super()._applyFormula(content, **kwargs)

        else:

            values = {}
            for property in self.rules.properties.values():

                if property.name in content and \
                   property.isAlreadyCalculated(content[property.name]):

                       values[property.name] = property.valueToPython(content[property.name])

                else:
                    if not property.isFormula(): continue

                    argContent = content[property.name] if property.name in content else property.DEFAULT_VALUE,

                    if property.type in ["object", "list"] and property.isNestedFormula():
                        argKwargs = kwargs | {"own" : content[property.name] \
                                              if property.name in content \
                                              else property.DEFAULT_VALUE}
                    else:
                        argKwargs = kwargs

                    value = property._applyFormula(argContent, **argKwargs)

                    values[property.name] = property.valueToPython(value)

                content.update(values)

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


#%%|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#region Dataframe


    def toDataframe(self, registers) -> DataFrame:

        data = []
        for register in registers:

            row = []
            for property in self.rules.properties.values():

                try: value = register[self.name][property.name]
                except KeyError: value = property.DEFAULT_VALUE

                row.append(value)

            data.append(row)

        return pd.DataFrame(data = data,
                            index = [register.id for register in registers],
                            columns = [property for property in self.rules.properties])