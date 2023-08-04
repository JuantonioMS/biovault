from typing import Any

from biovault.variable.type import Nominal


class Binomial(Nominal):


    @property
    def content(self):

        try: return self.info["rules"]["content"]
        except KeyError: return []



    def _checkRules(self, value: Any) -> list:

        checks = super()._checkRules(value)

        checks["onlyTwoItemsInContent"] = len(self.content) == 2

        return checks