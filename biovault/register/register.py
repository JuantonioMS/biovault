from pathlib import Path
from typing import Any

class Register:


    def __init__(self,
                 id: str = None,
                 jsonFile: Path = None,
                 variables: object = None) -> None:

        self._data = {}

        if id is not None:
            self._id = id
            self._data["biovaultID"] = id

        if jsonFile is not None:
            self._jsonFile = jsonFile if isinstance(jsonFile, Path) else Path(jsonFile)

        if variables is not None:
            self._variables = variables


    @property
    def id(self):

        try: return self._data["biovaultID"]
        except KeyError: return self._id



    def __getattribute__(self, attr: str) -> Any:

        if attr in super().__getattribute__("_data"): return self._data[attr]
        else: return super().__getattribute__(attr)



    def addData(self,
                key: str,
                value: Any) -> None:

        if key not in self._data:
            self._data[key] = value

        else:

            if isinstance(self._data[key], list):
                self._data[key].append(value)

            else:
                print(f"WARNING! {key} is already defined and is not a list")



    def __eq__(self, other: object) -> bool:

        if isinstance(other, Register):
            return self.id == other.id

        elif isinstance(other, str):
            return self.id == other

        else:
            return False