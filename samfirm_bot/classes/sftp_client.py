""" SFTP class """
# from os import path
#
# import asyncssh
#
# from samfirm_bot import SFTP_KEY, SFTP_PASS, SFTP_USER
#
#
# class SFTPClient:
#     """ SFTP management class """
#
#     def __init__(self, project):
#         self.url = f"https://osdn.net/projects/{project}/storage"
#         self.project = f"/storage/groups/s/sa/{project}"
#         self.conn = None
#         self.sftp = None
#
#     async def connect(self):
#         self.sftp = await self.connect_sftp()
#
#     async def connect_sftp(self):
#         if SFTP_KEY:
#             self.conn = await asyncssh.connect('storage.osdn.net',
#                                                username=SFTP_USER, client_keys=[SFTP_KEY])
#         elif SFTP_PASS:
#             self.conn = await asyncssh.connect('storage.osdn.net',
#                                                username=SFTP_USER, password=SFTP_PASS)
#         else:
#             print("You must provide a SFTP key or a password!")
#             exit(1)
#         return await self.conn.start_sftp_client()
#
#     async def makedirs(self, remotedir):
#         head, tail = path.split(remotedir)
#         if head and not await self.sftp.isdir(head):
#             await self.makedirs(head)
#         if tail:
#             await self.sftp.mkdir(remotedir)
#
#     async def upload(self, sftp_path, download_folder):
#         """ Upload a directory to SFTP"""
#         await self.makedirs(sftp_path)
#         await self.sftp.put(download_folder, sftp_path, recurse=True, preserve=True)
#
#     async def check(self, sftp_path):
#         """ Check if a directory exists"""
#         try:
#             exists = await self.sftp.isdir(sftp_path)
#         except asyncssh.sftp.SFTPError:
#             await self.connect()
#             exists = await self.sftp.isdir(sftp_path)
#         return exists
#
#     def __del__(self):
#         """ On destruction """
#         self.sftp.close()
#         self.conn.close()
