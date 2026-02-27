from typing import List
from .railway import Railway


class Route:
    def __init__(self, railways: List[Railway]):
        self.railways = railways
        self.stations = self.__build_path()

    def __build_path(self):
        if not self.railways:
            return []
        path = []
        first_railway = self.railways[0]
        stations = list(first_railway.stations)
        path.extend(stations)

        for railway in self.railways[1:]:
            current_end = path[-1]
            other_station = list(railway.stations)[0] if list(railway.stations)[0] != current_end\
                else list(railway.stations)[1]
            path.append(other_station)

        return path

    @property
    def total_distance(self):
        return sum(railway.length for railway in self.railways)

