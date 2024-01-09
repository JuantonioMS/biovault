import json
from pathlib import Path
import pandas as pd
from typing import Any, Iterator

from biovault.configuration import Configuration
from biovault.registers.register import Register

class Registers:

    """
    Clase de registros que alberga las registros de una base de datos.
    """

    def __init__(self, *args, configuration: Configuration = None) -> None:

        """
        Método de inicialización.

        Args:
            *args (Path): ficheros que componen la configuración, pueden ser .xlsx o .json.
            configuration (Configuration): instancia de configuración.
        """

        self._configuration = configuration

        self._registers = self._readFiles(*args)



    def _readFiles(self,
                   *args) -> dict[str : Register]:

        registers = {}
        for file in args:
            registers = self._updateRegisters(registers,
                                              self._readFile(file))

        return registers



    def _readFile(self,
                  file: Path) -> dict[str : dict[str : Any]]:

        if file.suffix == ".xlsx": return self._readExcel(file)
        elif file.suffix == ".json": return self._readJson(file)
        else: raise TypeError(f"{file.suffix} extension not valid")



    def _readExcel(self,
                   file: Path) -> dict[str : dict[str : Any]]:

        registers = {}
        with pd.ExcelFile(file) as file:

            for sheetName in file.sheet_names:

                dataframe = file.parse(sheetName)

                for _, row in dataframe.iterrows():

                    if sheetName in self._configuration.getVariablesNames(type = "list"):

                        if len(row.index) > 2:

                            register = Register({"ID" : row["ID"],
                                                 sheetName : [{column : value \
                                                               for column, value in zip(row.index, row.values) \
                                                               if column != "ID" and \
                                                                  not pd.isna(value) and \
                                                                  not (isinstance(value, str) and \
                                                                       value.lower() in ["nan", "none",
                                                                                         "ns", "nc",
                                                                                         "ns/nc", "nc/ns"])}]},
                                                configuration = self._configuration)

                        else:

                            register = Register({"ID" : row["ID"],
                                                 sheetName : [value \
                                                              for column, value in zip(row.index, row.values) \
                                                              if column != "ID" and \
                                                              not pd.isna(value) and \
                                                              not (isinstance(value, str) and \
                                                                   value.lower() in ["nan", "none",
                                                                                     "ns", "nc",
                                                                                     "ns/nc", "nc/ns"])]},
                                                configuration = self._configuration)

                    elif sheetName in self._configuration.getVariablesNames(type = "object"):

                        register = Register({"ID" : row["ID"],
                                             sheetName : {column : value \
                                                          for column, value in zip(row.index, row.values) \
                                                          if column != "ID" and \
                                                          not pd.isna(value) and \
                                                          not (isinstance(value, str) and \
                                                               value.lower() in ["nan", "none",
                                                                                 "ns", "nc",
                                                                                 "ns/nc", "nc/ns"])}},
                                            configuration = self._configuration)

                    else:

                        register = Register({column : value for column, value in zip(row.index, row.values)
                                                            if not pd.isna(value) and \
                                                            not (isinstance(value, str) and \
                                                                 value.lower() in ["nan", "none",
                                                                                   "ns", "nc",
                                                                                   "ns/nc", "nc/ns"])},
                                            configuration = self._configuration)

                    registers = self._updateRegisters(registers,
                                                    {row["ID"] : register})


        return registers


    def _readJson(self,
                  file: Path) -> dict[str : dict[str : Any]]:

        register = {}
        with open(file, "r") as file:
            data = json.load(file)

        register = Register(data, configuration = self._configuration)
        return {register.id : register}



    def _updateRegisters(self,
                         currentRegisters: dict[str : dict[str : Any]],
                         updateRegisters: dict[str : dict[str : Any]]) -> dict[str : dict[str : Any]]:

        for updateRegisterId, updateRegister in updateRegisters.items():

            if not updateRegisterId in currentRegisters:
                currentRegisters[updateRegisterId] = updateRegister

            else:
                currentRegisters[updateRegisterId] = currentRegisters[updateRegisterId] + updateRegister

        return currentRegisters



    def __iter__(self) -> Iterator:
        return iter(self._registers.values())