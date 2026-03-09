from exceptions.exceptions import LocomotiveUsingError
from compound.locomotive import Locomotive
from typing import List


class LocomotiveManager:
    def __init__(self):
        self.__qualification_level: int = 1
        self.__repaired_locomotives: int = 0
        self.__max_level: int = 5
        self.__locomotives: List[Locomotive] = []
        self.__numbers: list[int] = [i.number for i in self.__locomotives]

    @property
    def qualification_level(self):
        return self.__qualification_level

    def __upgrade_level(self):
        if self.__qualification_level + 1 > self.__max_level:
            self.__qualification_level = self.__max_level
        else:
            self.__qualification_level += 1

    @staticmethod
    def __service_locomotive(locomotive: Locomotive):
        locomotive.is_usable = True
        print("The locomotive has been serviced")

    @staticmethod
    def check_locomotive(locomotive: Locomotive):
        if not locomotive.check_state():
            LocomotiveManager.__service_locomotive(locomotive)
        else:
            print("All ok")






