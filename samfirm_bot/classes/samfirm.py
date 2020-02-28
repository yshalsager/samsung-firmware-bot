""" SamFirm wrapper class """
import asyncio
import json
import re
from datetime import datetime
from glob import glob
from os import path, makedirs
from shutil import rmtree
from zipfile import ZipFile

import aiohttp
from humanize import naturalsize

from samfirm_bot import PARENT_DIR, TG_LOGGER, WORK_DIR


class SamFirm:
    """ SamFirm wrapper """

    def __init__(self, loop):
        self.prefix = f"WINEDEBUG=fixme-all,err-all wine {PARENT_DIR}/SamFirm/SamFirm.exe"
        self.loop = loop
        self.session = aiohttp.ClientSession()
        self.regions = self.load_regions()
        self.models = []
        self.loop.create_task(self.models_loop())
        self.download_dir = f"{PARENT_DIR}/SamFirm/downloads"

    @staticmethod
    def load_regions():
        """fetch Samsung devices regions"""
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
        #     'Accept': 'application/json, text/javascript, */*; q=0.01',
        #     'X-Requested-With': 'XMLHttpRequest', 'Connection': 'keep-alive',
        #     'Referer': 'https://samdb.org/firmware/', 'Pragma': 'no-cache',
        #     'Cache-Control': 'no-cache',
        # }
        # async with self.session.get('https://samdb.org/ajax/regions?model=',
        #                             headers=headers) as response:
        #     try:
        #         data = json.loads(await response.text())
        #         regions = [i['text'].split(' ')[0] for i in data['results'][1:]]
        #         return regions
        #     except json.decoder.JSONDecodeError:
        #         TG_LOGGER.warning("Couldn't fetch regions!")
        with open(f'{WORK_DIR}/data/regions.txt', 'r') as regions_file:
            return regions_file.read().splitlines()

    async def load_models(self):
        """
        fetch Samsung devices models
        """
        async with self.session.get(
                'https://www.sammobile.com/wp-content/themes/sammobile-5/'
                'templates/fw-page/ajax/ajax.models.php?search') as response:
            try:
                data = json.loads(await response.text())
                models = [i['id'] for i in data]
                return models
            except json.decoder.JSONDecodeError:
                TG_LOGGER.warning("Couldn't fetch models!")

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
        date = datetime.strptime(re.search(r"(20[0-9]{6})", filename).group(1), '%Y%m%d').strftime('%Y-%m-%d')
        size = naturalsize(int(re.search(r"(?:Size: )(.*)(?: bytes)", output).group(1)))
        info = {"model": model, "system": version.split('/')[0],
                "csc": version.split('/')[1], "bootloader": version.split('/')[2],
                "date": date, "android": android_version,
                "filename": filename, "size": size}
        return info

    def download_update(self, model: str, region: str, version: str = None) -> str:
        """Check the latest available update"""
        download_path = f"{self.download_dir}/{model}/{region}/"
        command = f"{self.prefix} -model {model} -region {region}"
        if version:
            command += f" -version {version}"
        command += f" -autodecrypt -folder {download_path}"
        if path.exists(download_path):
            rmtree(download_path)
        makedirs(download_path)
        return command

    def get_downloaded(self, model: str, region: str):
        """Get downloaded file name"""
        try:
            return glob(f"{self.download_dir}/{model}/{region}/*.zip")[0]
        except IndexError:
            return None

    @staticmethod
    def extract_files(file):
        print(file)
        with ZipFile(file, 'r') as zip_file:
            files = [n for n in zip_file.namelist() if 'AP' not in n]
            zip_file.extractall(path='/'.join(file.split('/')[:-1]), members=files)
        return True

    async def models_loop(self):
        """ fetch models info every 12 hours """
        while True:
            TG_LOGGER.info("Refreshing models data")
            self.models = await self.load_models()
            await asyncio.sleep(60 * 60 * 12)
