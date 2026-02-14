from typing import List
from compound.locomotive import Locomotive
from compound.coach import Coach


class Compound:
    __compound_id_counter = 1

    def __init__(self, locomotive: Locomotive, coaches: List[Coach]):
        self.locomotive = locomotive
        self.coaches = sorted(coaches, key= lambda c: c.number)
        self.__compound_id = Compound.__compound_id_counter
        Compound.__compound_id_counter += 1

    @property
    def compound_id(self):
        return self.__compound_id

    def add_coach(self, coach: Coach):
        self.coaches.append(coach)
        self.coaches.sort(key= lambda c: c.number)

