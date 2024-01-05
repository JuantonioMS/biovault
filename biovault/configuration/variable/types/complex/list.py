from biovault.configuration.variable.types.complex import Complex

class List(Complex):


    def _completeVariableInfo(self, variable: dict) -> dict:

        from biovault.configuration.variable import Variable

        variable = super()._completeVariableInfo(variable)

        variable["rules"]["items"] = Variable(variable["rules"]["items"]).fabrica()

        return variable



    @property
    def jsonSchema(self) -> dict:

        schema = {"type" : "array"}
        for rule, value in self.jsonDumpFormat["rules"].items():

            if rule in ["required"]: continue

            if rule == "items":


                schema[rule] = self._variable["rules"]["items"].jsonSchema
                continue

            schema[rule] = value

        return schema