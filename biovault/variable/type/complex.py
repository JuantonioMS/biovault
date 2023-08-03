from biovault.variable import Variable


class Complex(Variable):


    @property
    def length(self):

        try:

            lowerInterval, upperInterval = self.info["rules"]["interval"].split(":")

            lowerBracket, lowerValue = lowerInterval[0], int(lowerInterval[1:])
            upperBracket, upperValue = upperInterval[-1], int(upperInterval[:-1])

            if lowerBracket == "(":
                if upperBracket == ")": return P.open(lowerValue, upperValue)
                else: return P.openclosed(lowerValue, upperValue)

            else:
                if upperBracket == ")": return P.closedopen(lowerValue, upperValue)
                else: return P.closed(lowerValue, upperValue)

        except KeyError:
            return P.open(-P.inf, P.inf)


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

    @property
    def values(self) -> list:
        try: return [Variable(value).getSpecificVariable() for value in self.info["values"]]
        except KeyError: return []