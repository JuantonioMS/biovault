import os
from pathlib import Path

from biovault.configuration.constants import SCRIPTS_FOLDER_NAME


class Scripts:


    def __init__(self, scripts: Path) -> None:

        #  If an link exists, it is deleted
        if SCRIPTS_FOLDER_NAME in os.listdir():
            os.system(f"rm -rf {SCRIPTS_FOLDER_NAME}")

        #  If there is a script folder, it is linked
        if scripts is not None:
            os.system(f"ln -s {scripts} {SCRIPTS_FOLDER_NAME}")