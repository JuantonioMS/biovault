from typing import Any

from biovault.variable.type import Nominal


class Binomial(Nominal):


    @property
    def content(self):

        try: return self.info["rules"]["content"]
        except KeyError: return []



    def _checkRules(self, value: Any) -> list:

        return [value in self.content,
                len(self.content) == 2] + \
               super()._checkRules(value)