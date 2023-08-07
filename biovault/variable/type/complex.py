import portion as P
from typing import Any

from biovault.variable import Variable


class Complex(Variable):


    def _checkRules(self, value: Any) -> list:

        checks = super()._checkRules(value)

        checks["haveCorrectLength"] = len(value) in self.length

        return checks


    @property
    def length(self) -> P:

        try:

            lowerInterval, upperInterval = self.info["rules"]["length"].split(":")

            lowerBracket, lowerValue = lowerInterval[0], float(lowerInterval[1:])
            upperBracket, upperValue = upperInterval[-1], float(upperInterval[:-1])

            if lowerBracket == "(":
                if upperBracket == ")": return P.open(lowerValue, upperValue)
                else: return P.openclosed(lowerValue, upperValue)

            else:
                if upperBracket == ")": return P.closedopen(lowerValue, upperValue)
                else: return P.closed(lowerValue, upperValue)

        except KeyError:
            return P.closed(1, P.inf)