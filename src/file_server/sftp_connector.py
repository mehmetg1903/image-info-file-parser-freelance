from pysftp import Connection, CnOpts


class SFTPConnector:
    def __init__(self, **kwargs):
        cnopts = CnOpts()
        cnopts.hostkeys = None
        self._sftp = Connection(host=kwargs["host"], username=kwargs["username"],
                                password=kwargs["password"], cnopts=cnopts)
        print("File server connection established...")
        self._folder = kwargs["folder"]

    def get_latest_file(self, folder=None):
        if folder is not None:
            self._sftp.chdir(folder)

        latest = 0
        latest_file = None

        for fileattr in self._sftp.listdir_attr():
            if fileattr.st_mtime > latest:
                latest = fileattr.st_mtime
                latest_file = fileattr.filename

        print(latest_file, "will be downloaded. It is the latest file")

        if latest_file is not None:
            self._sftp.get(latest_file, "../tmp/" + latest_file)

        self._sftp.close()
        return "../tmp/" + latest_file
