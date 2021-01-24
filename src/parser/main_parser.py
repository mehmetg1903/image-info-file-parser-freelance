import configparser
import pathlib
import shutil

from src.db.db_executer import DB
from src.file_server.file_downloader import FileDownloader
from src.parser.collin_parser import CollinParser
from src.parser.bexar_parser import BexarParser
from src.parser.parser_type import ParserType
from src.parser.tarrant_parser import TarrantParser


class MainParser:
    def __init__(self, config):
        self._main_config = config
        self._parser_type = ParserType.decide_type(self._main_config["SOURCE"]["name"])

        self._db = None

        self._parser_config = None
        self._parser = None

    def _load_parser_config(self):
        self._parser_config = configparser.ConfigParser()
        self._parser_config.read(
            str(pathlib.Path("../config/{}.ini".format(self._main_config["SOURCE"]["name"])).absolute()))

    def _prepare_parser(self):
        if self._parser_type == ParserType.Tarrant:
            self._parser = TarrantParser(
                self._main_config["GENERAL"]["download_folder"] + self._parser_config["FILE_SERVER"]["parse_file"])
        elif self._parser_type == ParserType.Collin:
            self._parser = CollinParser(
                self._main_config["GENERAL"]["download_folder"] + self._parser_config["FILE_SERVER"]["parse_file"])
        elif self._parser_type == ParserType.Bexar:
            self._parser = BexarParser(
                self._main_config["GENERAL"]["download_folder"] + self._parser_config["FILE_SERVER"]["parse_file"])

    def parse(self):
        tmp_path = pathlib.Path(self._main_config["GENERAL"]["download_folder"])
        tmp_path.mkdir(parents=True, exist_ok=True)
        self._load_parser_config()
        file_downloader = FileDownloader(self._main_config["GENERAL"]["download_folder"],
                                         **self._parser_config["FILE_SERVER"])

        if not eval(self._main_config["GENERAL"]["all"]):
            file_downloader.operate()
            self._prepare_parser()
            self._db = DB(self._parser_config["TABLE"]["name"], **self._main_config["DB"])
            self._parser.parse(self._db)

        else:
            for _ in file_downloader.operate_for_all():
                self._prepare_parser()
                self._db = DB(self._parser_config["TABLE"]["name"], **self._main_config["DB"])
                self._parser.parse(self._db)
        self._db.close()
        shutil.rmtree(tmp_path)
