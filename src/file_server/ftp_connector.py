from ftplib import FTP
import time
import re


class FTPConnector:
    def __init__(self, download_folder, **kwargs):
        self._ftp = FTP(kwargs["host"])
        self._ftp.login(user=kwargs["username"] if kwargs["username"] is not None else '',
                        passwd=kwargs["password"] if kwargs["password"] is not None else '')
        print("File server connection established...")
        self._folder = kwargs["folder"]
        self._download_folder = download_folder

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

        latest_path = self.download_latest_file(folder, latest, is_dir)
        return latest_path

    def download_latest_file(self, root_dir, latest, is_dir):
        if is_dir:
            print(latest + " is the most recent folder. Changing directory...")
            return self.get_latest_file(root_dir + latest + "/")
        else:
            print(latest, "will be downloaded...")
            dest_file = open(self._download_folder + latest, 'wb+')
            print("Retrieving the latest file...")
            self._ftp.retrbinary('RETR %s' % root_dir + latest, dest_file.write)
            print("Latest file is retrieved...")

        return self._download_folder + latest

    @staticmethod
    def parse_line(line):
        ls_parsed = re.sub(" +", " ", line).split(" ")
        latest = ls_parsed[-1]
        is_dir = "<DIR>" in ls_parsed
        return (latest, is_dir)

    def get_all_files(self, folder=None):
        if folder is not None:
            self._ftp.cwd(folder)
        lines = []
        self._ftp.dir("-t", lines.append)

        print("There are {} files to parse...".format(len(lines)))
        all_files = list(map(lambda x: FTPConnector.parse_line(x), lines))

        for file in all_files:
            yield file

    def close(self):
        self._ftp.close()
