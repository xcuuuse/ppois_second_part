import json
from typing import List
from pathlib import Path
from compound.locomotive import Locomotive
from compound.coach import Coach
from railway.route import Route, Station
from enums.enums import TrainState
from exceptions.exceptions import InvalidStateError


class Compound:
    __compound_id_counter = 1

    def __init__(self, locomotive: Locomotive, coaches: List[Coach], compound_id: int = None):
        self.locomotive = locomotive
        self.coaches = sorted(coaches, key= lambda c: c.number)
        if compound_id is None:
            self.__compound_id = Compound.__compound_id_counter
            Compound.__compound_id_counter += 1
        else:
            self.__compound_id = compound_id
            if compound_id >= Compound.__compound_id_counter:
                Compound.__compound_id_counter = compound_id + 1
        self.__current_pos = 0
        self.state = TrainState.STOPPED

    @property
    def compound_id(self):
        return self.__compound_id

    @property
    def current_pos(self):
        return self.__current_pos

    def add_coach(self, coach: Coach):
        self.coaches.append(coach)
        self.coaches.sort(key=lambda c: c.number)

    def move_along_route(self, route: Route):
        if self.state != TrainState.STOPPED and self.state != TrainState.AT_STATION:
            raise InvalidStateError("Cannot move from this state")
        self.state = TrainState.MOVING
        if self.__current_pos >= len(route.stations):
            print("The compound has completed the route")
            return
        current_station = route.stations[self.__current_pos]
        print(f"The compound {self.__compound_id} arrived at {current_station.name}")
        self.__current_pos += 1

        if self.__current_pos < len(route.stations):
            next_station = route.stations[self.__current_pos]
            print(f"The compound {self.__compound_id} is moving towards {next_station.name}")
        else:
            print(f"The compound {self.__compound_id} has completed the route")
            self.state = TrainState.STOPPED

    def process_station_actions(self):
        if self.state != TrainState.MOVING:
            raise InvalidStateError("Cannot process station actions from this state")
        self.state = TrainState.AT_STATION
        for coach in self.coaches:
            coach.free_coach()

    def check_state(self):
        if not self.locomotive.check_state():
            self.state = TrainState.MAINTENANCE
        self.state = TrainState.STOPPED


