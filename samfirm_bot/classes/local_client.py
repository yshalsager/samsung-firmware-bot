""" SamFirm Bot local storage class"""
import shutil
from datetime import datetime
from os import path, mkdir
from pathlib import Path


class LocalClient:
    """ Local Storage management class """

    def __init__(self, local_storage_path, web_storage):
        self.path = local_storage_path
        self.root = Path(local_storage_path)
        self.website = web_storage

    async def move(self, _source, _dest):
        """Move path to web storage"""
        dest = self.root / _dest
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
        return str(_path).replace(self.path, self.website)

    async def get_free_space(self):
        """Get free disk space percentage"""
        disk_usage = shutil.disk_usage(self.root)
        # human_disk_usage = {
        #     'free': naturalsize(disk_usage.free),
        #     'used': naturalsize(disk_usage.used),
        #     'total': naturalsize(disk_usage.total)
        # }
        # print(human_disk_usage)
        percent = (disk_usage.used / disk_usage.total) * 100.0
        return percent

    async def has_space(self):
        """Return true if the disk space is more than 20% free"""
        free_space_percent = await self.get_free_space()
        return bool(free_space_percent > 20)

    async def list_dirs(self):
        """Return a directory of directories sorted by creation time"""
        dirs = {datetime.fromtimestamp(item.stat().st_ctime): item
                for item in self.root.iterdir()
                if item.is_dir()}
        sorted_dirs = {k: v for k, v in sorted(dirs.items(), key=lambda item: item[0])}
        return sorted_dirs

    async def cleanup(self):
        """Clean up storage directory until disk available space is more than 75"""
        dirs = await self.list_dirs()
        for directory in dirs.values():
            if await self.get_free_space() < 75:
                print(f"Deleting: {directory}")
                shutil.rmtree(directory)
