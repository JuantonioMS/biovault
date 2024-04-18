from biovault.database.variables.variable.type.type import Type


class Complex(Type):


    def isFormula(self) -> bool:
        return (super().isFormula() or self.isNestedFormula())


from biovault.database.variables.variable.type.complex.list import List
from biovault.database.variables.variable.type.complex.object import Object
from biovault.database.variables.variable.type.complex.multilabel import Multilabel
from biovault.database.variables.variable.type.complex.multivalue import Multivalue