from typing import Set
from .station import Station


class Railway:
    def __init__(self, stations: Set[Station], length: float):
        if len(stations) != 2:
            raise ValueError("Railway must connect exactly 2 stations")
        self.stations = frozenset(stations)
        self.length = length

