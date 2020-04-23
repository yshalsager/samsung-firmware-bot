""" SamFirm Bot local storage class"""
import shutil
from os import path, mkdir
from pathlib import Path

from samfirm_bot import WEB_STORAGE, LOCAL_STORAGE


class LocalClient:
    """ Local Storage management class """

    def __init__(self, local_storage_path, web_storage):
        self.root = Path(local_storage_path)
        self.website = web_storage

    async def move(self, _source, _dest):
        """Move path to web storage"""
        dest = self.root / _dest
        print(f"source: {_source}")
        print(f"dest: {dest}")
        try:
            shutil.move(_source, dest)
        except FileNotFoundError as err:
            print(f"Error: Couldn't move {_source} to {dest}\n{err}")
        return f"{self.website}/{_dest}"

    async def check(self, _path):
        """Check if a path exists"""
        if _path != self.root.name:
            directory = self.root / _path
            return directory.exists()

    async def makedirs(self, _path):
        """create directories"""
        head, tail = path.split(_path)
        if head and not self.check(head):
            await self.makedirs(head)
        if tail:
            try:
                mkdir(f"{self.root}/{_path}/")
                print(f"mkdir: {self.root}/{_path}")
            except FileExistsError:
                pass

    async def listdir(self, _path):
        """List a directory"""
        directory = self.root / _path
        return [x for x in directory.iterdir() if x.is_dir()]

    async def get_url(self, _path):
        """Get download URL of a path"""
        return str(_path).replace(LOCAL_STORAGE, WEB_STORAGE)
