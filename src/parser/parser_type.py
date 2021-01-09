import enum


class ParserType(enum.Enum):
    Tarrant = 1
    Collin = 2
    Bexar = 3

    _parser_types = [Tarrant, Collin, Bexar]

    @staticmethod
    def parser_types():
        return ParserType._parser_types

    @staticmethod
    def decide_type(name):
        if "tarrant" == name.lower():
            return ParserType.Tarrant
        if "collin" == name.lower():
            return ParserType.Collin
        if "bexar" == name.lower():
            return ParserType.Bexar
