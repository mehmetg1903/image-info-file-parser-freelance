import enum


class FileSource(enum.Enum):
    FTP = 1
    SFTP = 2

    _all_sources = [FTP, SFTP]

    @staticmethod
    def file_sources():
        return FileSource._all_sources
