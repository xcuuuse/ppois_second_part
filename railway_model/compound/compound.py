from typing import List
from compound.locomotive import Locomotive
from compound.coach import Coach
from railway.route import Route, Station


class Compound:
    __compound_id_counter = 1

    def __init__(self, locomotive: Locomotive, coaches: List[Coach]):
        self.locomotive = locomotive
        self.coaches = sorted(coaches, key= lambda c: c.number)
        self.__compound_id = Compound.__compound_id_counter
        Compound.__compound_id_counter += 1
        self.__current_pos = 0

    @property
    def compound_id(self):
        return self.__compound_id

    def add_coach(self, coach: Coach):
        self.coaches.append(coach)
        self.coaches.sort(key= lambda c: c.number)

    def move_along_route(self, route: Route):
        if self.__current_pos >= len(route.stations):
            print("The compound has completed the route")
        current_station = route.stations[self.__current_pos]
        print(f"The compound {self.__compound_id} arrived at {current_station.name}")
        self.__current_pos += 1

        if self.__current_pos < len(route.stations):
            next_station = route.stations[self.__current_pos]
            print(f"The compound {self.__compound_id} is moving towards {next_station.name}")
        else:
            print(f"The compound {self.__compound_id} has completed the route")

    def process_station_actions(self, station: Station):
        pass