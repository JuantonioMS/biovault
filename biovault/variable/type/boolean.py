from typing import Any

from biovault.variable.type import Binomial
from biovault.conf.constants import BOOLEAN_TRUE_LIKE, BOOLEAN_FALSE_LIKE


class Boolean(Binomial):


    def _transformValue(self, value: Any) -> bool:

        if value in BOOLEAN_TRUE_LIKE: return True
        elif value in BOOLEAN_FALSE_LIKE: return False
        else:
            print("OJO que no está", value)
            return False