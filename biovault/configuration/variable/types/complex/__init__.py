from biovault.configuration.variable.types import Types

class Complex(Types):


    def isFormula(self) -> bool:
        return (super().isFormula() or self.isNestedFormula())