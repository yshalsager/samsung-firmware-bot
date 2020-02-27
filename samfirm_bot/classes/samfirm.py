""" SamFirm wrapper class """
import re
from datetime import datetime

from humanize import naturalsize

from samfirm_bot import PARENT_DIR


class SamFirm:
    """ SamFirm wrapper """

    def __init__(self):
        self.prefix = f"WINEDEBUG=fixme-all,err-all wine {PARENT_DIR}/SamFirm/SamFirm.exe"

    def check_update(self, model: str, region: str, version: str = None) -> str:
        """Check the latest available update"""
        command = f"{self.prefix} -c -model {model} -region {region}"
        if version:
            command += f" -version {version}"
        return command

    @staticmethod
    def parse_output(output: str) -> dict:
        """Parse SamFirm output"""
        model = re.search(r"(?:Model: )(.*)", output).group(1)
        version = re.search(r"(?:Version: )(.*)", output).group(1)
        android_version = re.search(r"(?:OS: )(.*)", output).group(1).replace('(', ' (')
        filename = re.search(r"(?:Filename: )(.*)", output).group(1)
        date = datetime.strptime(filename.split('_')[2][:8], '%Y%m%d').strftime('%Y-%m-%d')
        size = naturalsize(int(re.search(r"(?:Size: )(.*)(?: bytes)", output).group(1)))
        info = {"model": model, "system": version.split('/')[0],
                "csc": version.split('/')[1], "bootloader": version.split('/')[2],
                "date": date, "android": android_version,
                "filename": filename, "size": size}
        return info
