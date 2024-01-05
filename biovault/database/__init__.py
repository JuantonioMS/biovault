import jsonschema
from pathlib import Path
from typing import Union

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
                 registers: Union[Path, list[Path]] = None) -> None:

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

        if not configuration is None:
            self._configuration = self._readConfiguration(configuration)

        if not registers is None:
            self._registers = self._readRegisters(registers)



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
            return Registers(*registers)

        else:
            if registers.is_dir(): return Registers(*list(registers.iterdir()))
            else: return Registers(registers)



    def checkRegisters(self) -> dict:

        schema = BioVaultValidator(self._configuration.jsonSchema())

        errors = {}
        for register in self._registers:

            validationErrors = sorted(schema.iter_errors(register._data),
                            key = lambda x: x.path)

            if validationErrors: errors[register._data["ID"]] = validationErrors

        return errors



    def checkRegistersToTsv(self,
                            file: Path) -> None:

        errors = self.checkRegisters()

        msg = ["\t".join(["ID",
                          "Variable",
                          "Value",
                          "Validator",
                          "Message"])]
        for id, errors in errors.items():

            for error in errors:

                name = ".".join(list(map(str,error.path)))
                if error.validator == "required":
                    if name: name += "." + error.message.split(" ")[0].strip("'")
                    else: name = error.message.split(" ")[0].strip("'")

                instance = str(error.instance) if error.validator != "required" else "None"

                msg.append("\t".join([str(id),
                                      name,
                                      instance,
                                      error.validator,
                                      error.message]))

        with open(file, "w") as outfile:
            outfile.write("\n".join(msg))