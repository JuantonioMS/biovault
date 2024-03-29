import jsonschema
from pathlib import Path
import pandas as pd
from typing import Any, Union, Iterator
import os

from biovault.validator import BioVaultValidator
from biovault.configuration import Configuration
from biovault.registers import Registers
class Database:

    """
    Clase de base detos que combina los archivos de configuración y de registros en una sola instancia para
    ejecutar operaciones conjuntas y globales de forma sencilla.
    """

    def __init__(self,
                 configuration: Union[Path, list[Path]] = None,
                 registers: Union[Path, list[Path]] = None,
                 scripts: Path = None) -> None:

        """
        Método de inicialización.

        Args:
            configuration (Union[Path, list[Path]]): ruta al fichero/ficheros/directorio de configuración.
                Path (directorio): directorio con los archivos de configuración.
                Path (fichero)   : archivo de configuración.
                list[Path]       : listado de archivos de configuración.

            registers (Union[Path, list[Path]]): ruta al fichero/ficheros/directorio de registro.
                Path (directorio): directorio con los archivos de registro.
                Path (fichero)   : archivo de registro.
                list[Path]       : listado de archivos de registro.
        """

        self._scripts = self._readScripts(scripts)

        if not configuration is None:
            self._configuration = self._readConfiguration(configuration)

        if not registers is None:
            self._registers = self._readRegisters(registers)

        self._registers._executeFormulas()



    def _readScripts(self,
                     scripts: Path) -> Path:


        if "scripts" in os.listdir():
            os.system("rm -rf scripts")

        if not scripts is None:
            os.system(f"ln -s {scripts} scripts")

        return scripts



    def _readConfiguration(self,
                           configuration: Union[Path, list[Path]]) -> Configuration:

        """
        Método para cargar los archivos de configuración instanciándolos en un objeto Configuration.

        Args:
            configuration (Union[Path, list[Path]]): ruta al fichero/ficheros/directorio de configuración.
                Path (directorio): directorio con los archivos de configuración.
                Path (fichero)   : archivo de configuración.
                list[Path]       : listado de archivos de configuración.

        Returns:
            Configuration: Objeto de la clase Configuration
        """

        if isinstance(configuration, list):
            return Configuration(*configuration)

        else:
            if configuration.is_dir(): return Configuration(*list(configuration.iterdir()))
            else: return Configuration(configuration)



    def _readRegisters(self,
                       registers: Union[Path, list[Path]]) -> Registers:

        """
        Método para cargar los archivos de registro instanciándolos en un objeto Registers.

        Args:
            registers (Union[Path, list[Path]]): ruta al fichero/ficheros/directorio de registro.
                Path (directorio): directorio con los archivos de registro.
                Path (fichero)   : archivo de registro.
                list[Path]       : listado de archivos de registro.

        Returns:
            Registers: Objeto de la clase Registers
        """

        if isinstance(registers, list):
            return Registers(*registers, configuration = self._configuration)

        else:
            if registers.is_dir(): return Registers(*list(registers.iterdir()), configuration = self._configuration)
            else: return Registers(registers, configuration = self._configuration)



    def iterConfiguration(self) -> Iterator:
        return iter(self._configuration)



    def iterRegisters(self) -> Registers:
        return iter(self._registers)


    def check(self) -> pd.DataFrame:
        return self._registers.check(self._configuration)

    def checkRules(self) -> pd.DataFrame:
        return self._registers.checkRules(self._configuration)

    def checkControls(self) -> pd.DataFrame:
        return self._registers.checkControls(self._configuration)



    def toDataframe(self) -> pd.DataFrame:

        from biovault.configuration.variable.types.complex.list import List
        from biovault.configuration.variable.types.complex.object import Object
        from biovault.configuration.variable.types.complex.multilabel import Multilabel
        from biovault.configuration.variable.types.simple.numerical.date import Date

        dataframe = pd.DataFrame(index = [register.id for register in self._registers])

        for variable in self._configuration:

            if isinstance(variable, (List, Object, Date)) and not isinstance(variable, Multilabel): continue

            dataframe = pd.concat([dataframe,
                                   variable.variableToDataframe(self._registers)],
                                  axis = "columns",
                                  join = "inner",
                                  ignore_index = False,
                                  verify_integrity = True)

        return dataframe



    def filter(self,
               variable: str,
               sentence: str) -> None:

        self._registers.filter(variable, sentence)



    def restore(self) -> None:

        self._registers.restore()



    def __del__(self) -> None:

        if "scripts" in os.listdir():
            os.system("rm -rf scripts")