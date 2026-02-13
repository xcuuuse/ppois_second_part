from compound.locomotive import Locomotive
from compound.coach import Coach


class Compound:
    __compound_id_counter = 1

    def __init__(self, locomotive: Locomotive, coaches: list[Coach]):
        self.locomotive = locomotive
        self.coaches = coaches
        self.__compound_id = Compound.__compound_id_counter
        Compound.__compound_id_counter += 1

    @property
    def compound_id(self):
        return self.__compound_id