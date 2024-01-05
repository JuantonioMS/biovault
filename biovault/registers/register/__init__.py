class Register:


    def __init__(self, data: dict) -> None:
        self._data = data


    def _addData(self, data: dict) -> None:
        self._data.update(data)
