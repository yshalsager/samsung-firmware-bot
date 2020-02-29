""" SourceForge class """
from os import path

import asyncssh

from samfirm_bot import SF_KEY, SF_PASS, SF_USER


class SourceForge:
    """ SourceForge management class """

    def __init__(self, project):
        self.url = f"https://sourceforge.net/projects/{project}"
        self.project = f"/home/frs/project/{project}"
        self.conn = None
        self.sftp = None

    async def connect(self):
        self.sftp = await self.connect_sftp()

    async def connect_sftp(self):
        if SF_KEY:
            self.conn = await asyncssh.connect('frs.sourceforge.net',
                                               username=SF_USER, client_keys=[SF_KEY])
        elif SF_PASS:
            self.conn = await asyncssh.connect('frs.sourceforge.net',
                                               username=SF_USER, password=SF_PASS)
        else:
            print("You must provide a SF key or a password!")
            exit(1)
        return await self.conn.start_sftp_client()

    async def makedirs(self, remotedir):
        head, tail = path.split(remotedir)
        if head and not await self.sftp.isdir(head):
            await self.makedirs(head)
        if tail:
            await self.sftp.mkdir(remotedir)

    async def upload(self, sf_path, download_folder):
        """ Upload a directory to SourceForge"""
        await self.makedirs(sf_path)
        await self.sftp.put(download_folder, sf_path, recurse=True, preserve=True)

    def __del__(self):
        """ On destruction """
        self.sftp.close()
        self.conn.close()
