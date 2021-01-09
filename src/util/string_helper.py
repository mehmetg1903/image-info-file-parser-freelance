import re


def remove_multiple_spaces(string):
    return re.sub(" +", " ", string)


def trim(string):
    return string.strip()
