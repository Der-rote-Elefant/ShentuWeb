from enum import Enum


class Direction(Enum):
    LONG = 0
    SHORT = 1

class Offset(Enum):
    OPEN = "开"
    CLOSE = "平"
    CLOSETODAY = "平今"
    CLOSEYESTERDAY = "平昨"