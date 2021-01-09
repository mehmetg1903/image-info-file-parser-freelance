from src.file_server.file_source import FileSource
from src.file_server.ftp_connector import FTPConnector
from src.file_server.sftp_connector import SFTPConnector
import zipfile
import shutil


class FileDownloader:
    _valid_files = ["txt", ".csv", ".xml"]

    def __init__(self, **kwargs):
        self._source = FileSource.SFTP if eval(kwargs["use_ssl"]) else FileSource.FTP
        self._kwargs = kwargs
        self._connector = None

    def _connect(self):
        if self._source == FileSource.SFTP:
            self._connector = SFTPConnector(**self._kwargs)
        elif self._source == FileSource.FTP:
            self._connector = FTPConnector(**self._kwargs)

    def _get_most_recent_file(self):
        return self._connector.get_latest_file(self._kwargs["folder"])

    def operate(self, ):
        self._connect()
        latest_file = self._get_most_recent_file()
        # latest_file = "../tmp/1.zip"
        # latest_file = "../tmp/an_12_21__12_23_2020.zip"
        self._extract_file(latest_file)

    @staticmethod
    def _check_type(file_name):
        return any([file_name.endswith(f_type) for f_type in FileDownloader._valid_files])

    def _extract_file(self, latest_file):
        with zipfile.ZipFile(latest_file, 'r') as zip_ref:
            file_to_open = list(filter(lambda x: FileDownloader._check_type(x.filename), zip_ref.filelist))[0]
            with zip_ref.open(file_to_open.filename) as zip_file, \
                    open("../tmp/" + self._kwargs["parse_file"], "wb+") as wr_file:
                shutil.copyfileobj(zip_file, wr_file)

        print("zip file extracted...")
