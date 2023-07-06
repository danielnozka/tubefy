from json import JSONEncoder

from ..typing import JsonType


class ServerJsonEncoder:

    @staticmethod
    def encode(json_obj: JsonType) -> bytes:

        return JSONEncoder().encode(json_obj).encode('utf-8')
