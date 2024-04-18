from biovault.database.variables.variable import Variable


class Type(Variable):


    def __init__(self, object: Variable) -> None:
        self.__dict__.update(object.__dict__)