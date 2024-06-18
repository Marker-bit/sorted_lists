from enum import Enum


class ResponseType(str, Enum):
    CALCULATED = "CALCULATED"
    FOUND = "FOUND"
