import os
import shutil
import zipfile

from src.file_server.file_source import FileSource
from src.file_server.ftp_connector import FTPConnector
from src.file_server.sftp_connector import SFTPConnector


class FileDownloader:
    _valid_files = ["txt", ".csv", ".xml"]

    def __init__(self, download_folder, **kwargs):
        self._source = FileSource.SFTP if eval(kwargs["use_ssl"]) else FileSource.FTP
        self._kwargs = kwargs
        self._connector = None
        self._download_folder = download_folder

    def _connect(self):
        if self._connector is None:
            if self._source == FileSource.SFTP:
                self._connector = SFTPConnector(self._download_folder, **self._kwargs)
            elif self._source == FileSource.FTP:
                self._connector = FTPConnector(self._download_folder, **self._kwargs)

    def close(self):
        self._connector.close()

    def _get_most_recent_file(self):
        return self._connector.get_latest_file(self._kwargs["folder"])

    def operate(self):
        self._connect()
        self._clear_folder()
        latest_file = self._get_most_recent_file()
        self.close()
        self._extract_file(latest_file)

    def operate_for_all(self):
        self._connect()
        for file_name, is_dir in self._connector.get_all_files(self._kwargs["folder"]):
            self._clear_folder()
            file_path = self._connector.download_latest_file(self._kwargs["folder"], file_name, is_dir)
            self._extract_file(file_path)
            yield

    def _clear_folder(self):
        for filename in os.listdir(self._download_folder):
            filepath = os.path.join(self._download_folder, filename)
            try:
                shutil.rmtree(filepath)
            except OSError:
                os.remove(filepath)

    @staticmethod
    def _check_type(file_name):
        return any([file_name.endswith(f_type) for f_type in FileDownloader._valid_files])

    def _extract_file(self, latest_file):
        with zipfile.ZipFile(latest_file, 'r') as zip_ref:
            file_to_open = list(filter(lambda x: FileDownloader._check_type(x.filename), zip_ref.filelist))[0]
            with zip_ref.open(file_to_open.filename) as zip_file, \
                    open(self._download_folder + self._kwargs["parse_file"], "wb+") as wr_file:
                shutil.copyfileobj(zip_file, wr_file)

        print("zip file extracted...")
