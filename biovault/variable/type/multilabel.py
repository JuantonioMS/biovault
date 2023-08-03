from typing import Any

from biovault.conf.constants import MULTILABEL_SEPARATOR
from biovault.variable.type import Nominal


class Multilabel(Nominal):


    def _transformValue(self,
                        value: Any) -> list:

        return list(map(lambda x: x.lower().lstrip(" ").rstrip(" "),
                        value.split(MULTILABEL_SEPARATOR)))