from typing import Any
import portion as P

from biovault.variable import Variable


class Number(Variable):


    def _checkRules(self, value: Any) -> list:

        auxCheck = super()._checkRules(value)

        return auxCheck + [value in self.interval]


    @property
    def interval(self) -> P:

        try:

            lowerInterval, upperInterval = self.info["rules"]["interval"].split(":")

            lowerBracket, lowerValue = lowerInterval[0], float(lowerInterval[1:])
            upperBracket, upperValue = upperInterval[-1], float(upperInterval[:-1])

            if lowerBracket == "(":
                if upperBracket == ")": return P.open(lowerValue, upperValue)
                else: return P.openclosed(lowerValue, upperValue)

            else:
                if upperBracket == ")": return P.closedopen(lowerValue, upperValue)
                else: return P.closed(lowerValue, upperValue)

        except KeyError:
            return P.open(-P.inf, P.inf)



    def _transformValue(self, value: Any) -> int:
        return int(value)