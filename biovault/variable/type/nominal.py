from typing import Any

from biovault.variable.type import String


class Nominal(String):


    @property
    def content(self):

        try: return self.info["rules"]["content"]
        except KeyError: return []



    def _checkRules(self, value: Any) -> list:

        return [value in self.content if self.content else True] + \
               super()._checkRules(value)



    def _transformValue(self, value: Any) -> str:
        return super()._transformValue(value).lower()