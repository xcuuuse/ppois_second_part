from exceptions.exceptions import LocomotiveUsingError
from compound.locomotive import Locomotive


class LocomotiveManager:
    def __init__(self):
        self.__qualification_level: int = 1
        self.__repaired_locomotives: int = 0
        self.__max_level: int = 5
        self.__locomotives: list[Locomotive] = []
        self.__numbers: list[int] = [i.number for i in self.__locomotives]

    def upgrade_level(self):
        if self.__qualification_level + 1 > self.__max_level:
            self.__qualification_level = self.__max_level
        else:
            self.__qualification_level += 1

    def add_locomotive(self, locomotive: Locomotive):
        self.__locomotives.append(locomotive)

    def service_locomotive(self, locomotive: Locomotive):
        if locomotive.number not in self.__numbers:
            raise LocomotiveUsingError("The locomotive does not exist")
        locomotive.get_service()
        self.__repaired_locomotives += 1
        if self.__repaired_locomotives % 10 == 0:
            self.upgrade_level()






