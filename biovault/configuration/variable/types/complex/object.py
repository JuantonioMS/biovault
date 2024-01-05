from biovault.configuration.variable.types.complex import Complex

class Object(Complex):


    def _completeVariableInfo(self, variable: dict) -> dict:

        from biovault.configuration.variable import Variable

        variable = super()._completeVariableInfo(variable)

        aux = []
        for property in variable["rules"]["properties"]:
            aux.append(Variable(property).fabrica())

        variable["rules"]["properties"] = aux

        return variable



    @property
    def jsonSchema(self) -> dict:

        schema = {"type" : "object"}
        for rule, value in self.jsonDumpFormat["rules"].items():

            if rule in ["required"]: continue

            if rule == "properties":

                aux = {}
                for property in value:
                    aux[property.name] = property.jsonSchema

                schema[rule] = aux
                continue

            schema[rule] = value

        schema["required"] = [property.name for property in self._variable["rules"]["properties"] if property.jsonDumpFormat["rules"]["required"]]

        return schema
