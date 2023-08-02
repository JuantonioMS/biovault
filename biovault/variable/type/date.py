from datetime import datetime
from typing import Any

from biovault.variable import Variable
from biovault.conf.constants import DATE_FORMAT


class Date(Variable):

    def _transformValue(self, value: Any) -> str:
        return datetime.strptime(value, self.sourceFormat).strftime(DATE_FORMAT)