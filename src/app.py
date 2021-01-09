import configparser
import pathlib
import datetime

from src.parser.main_parser import MainParser

if __name__ == '__main__':
    print("Started...")
    config = configparser.ConfigParser()
    config.read(pathlib.Path("../config/config.ini"))

    main_parser = MainParser(config)
    main_parser.parse()
    print("Finished...")
