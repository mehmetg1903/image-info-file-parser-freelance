from ftplib import FTP
import time
import re


class FTPConnector:
    def __init__(self, **kwargs):
        self._ftp = FTP(kwargs["host"])
        self._ftp.login(user=kwargs["username"] if kwargs["username"] is not None else '',
                        passwd=kwargs["password"] if kwargs["password"] is not None else '')
        print("File server connection established...")
        self._folder = kwargs["folder"]

    def _is_dir(self, file_name):
        return self._ftp.size(file_name) is None

    def get_latest_file(self, folder=None):
        if folder is not None:
            self._ftp.cwd(folder)
        lines = []
        self._ftp.dir("-t", lines.append)
        lines.sort(key=lambda x: time.strptime(' '.join(x.split()[0:2]), '%m-%d-%y %H:%M%p'))

        ls_parsed = re.sub(" +", " ", lines[-1]).split(" ")
        latest = ls_parsed[-1]
        is_dir = "<DIR>" in ls_parsed

        if is_dir:
            print(latest + " is the most recent folder. Changing directory...")
            return self.get_latest_file(latest)
        else:
            print(latest, "will be downloaded...")
            dest_file = open("../tmp/" + latest, 'wb+')
            print("Retrieving the latest file...")
            self._ftp.retrbinary('RETR %s' % latest, dest_file.write)
            print("Latest file is retrieved...")

        self._ftp.close()
        return "../tmp/" + latest
