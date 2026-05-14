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
        start = next((s for s in stations if s.name == "O"), stations[0])
        end = next(s for s in stations if s != start)
        path.extend([start, end])

        for railway in self.railways[1:]:
            current_end = path[-1]
            other_station = next(s for s in railway.stations if s != current_end)
            path.append(other_station)
        return path

    @property
    def total_distance(self):
        return sum(railway.length for railway in self.railways)

