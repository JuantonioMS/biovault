from dataclasses import dataclass
import pandas as pd
from typing import Any


@dataclass
class Check:

    id: str
    variable: str
    value : Any
    validator : str
    message   : str

    def print_info(self):
        return pd.Series({"ID"        : self.id,
                          "Section"   : self.__class__.__name__.lower(),
                          "Variable"  : self.variable,
                          "Value"     : self.value,
                          "Validator" : self.validator,
                          "Message"   : self.message})



class Control(Check): pass



class Rule(Check): pass