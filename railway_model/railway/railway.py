from .station import Station


class Railway:
    def __init__(self, stations: set[Station], length: float):
        self.stations = frozenset(stations)
        self.length = length

