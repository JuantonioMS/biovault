import portion as P

from biovault.variable.type import Float


class Percentage(Float):


    @property
    def interval(self) -> P:

        auxInterval = super().interval

        if auxInterval == P.open(-P.inf, P.inf):
            auxInterval = P.closed(0, 1)

        return auxInterval