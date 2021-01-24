from pysftp import Connection, CnOpts
import stat


class SFTPConnector:
    def __init__(self, download_folder, **kwargs):
        cnopts = CnOpts()
        cnopts.hostkeys = None
        self._sftp = Connection(host=kwargs["host"], username=kwargs["username"],
                                password=kwargs["password"], cnopts=cnopts)
        print("File server connection established...")
        self._folder = kwargs["folder"]
        self._download_folder = download_folder

    def get_latest_file(self, folder=None):
        if folder is not None:
            self._sftp.chdir(folder)

        latest = 0
        latest_file = None

        is_dir = False

        for fileattr in self._sftp.listdir_attr():
            if fileattr.st_mtime > latest:
                is_dir = stat.S_ISDIR(fileattr.st_mode)
                latest = fileattr.st_mtime
                latest_file = fileattr.filename

        print(latest_file, "will be downloaded. It is the latest file")
        latest_downloaded = self.download_latest_file(folder, latest_file, is_dir)

        return latest_downloaded

    def download_latest_file(self, root_dir, latest, is_dir):
        if latest is not None:
            if is_dir:
                print(latest + " is the most recent folder. Changing directory...")
                return self.get_latest_file(latest)
            print(latest, "will be downloaded...")
            self._sftp.get(self._folder + latest, self._download_folder + latest)

        return self._download_folder + latest

    def get_all_files(self, folder=None):
        if folder is not None:
            self._sftp.chdir(folder)

        all_files = list(
            map(lambda x: (x.filename, stat.S_ISDIR(x.st_mode)), self._sftp.listdir_attr()))
        for e in all_files:
            yield e

    def close(self):
        self._sftp.close()
