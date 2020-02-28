""" SourceForge class """
import pysftp

from samfirm_bot import SF_KEY, SF_PASS, SF_USER


class SourceForge:
    """ SourceForge management class """

    def __init__(self, project):
        self.url = f"https://sourceforge.net/projects/{project}"
        self.project = f"/home/frs/project/{project}"
        self.sftp = self.connect_sftp()
        self.sftp.cd(self.project)

    @staticmethod
    def connect_sftp():
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        if SF_KEY:
            return pysftp.Connection('frs.sourceforge.net', username=SF_USER,
                                     private_key=SF_KEY, cnopts=cnopts)
        elif SF_PASS:
            return pysftp.Connection('frs.sourceforge.net', username=SF_USER,
                                     password=SF_PASS, cnopts=cnopts)
        else:
            print("You must provide a SF key or a password!")
            exit(1)

    def __del__(self):
        """ On destruction """
        self.sftp.close()
