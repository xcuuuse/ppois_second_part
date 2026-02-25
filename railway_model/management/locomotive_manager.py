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

    def __upgrade_level(self):
        if self.__qualification_level + 1 > self.__max_level:
            self.__qualification_level = self.__max_level
        else:
            self.__qualification_level += 1

    def add_locomotive(self, locomotive: Locomotive):
        self.__locomotives.append(locomotive)

    def __service_locomotive(self, locomotive: Locomotive):
        if locomotive.number not in self.__numbers:
            raise LocomotiveUsingError("The locomotive does not exist")
        locomotive.get_service()
        self.__repaired_locomotives += 1
        if self.__repaired_locomotives % 10 == 0:
            self.__upgrade_level()

        print("The locomotive has been serviced")

    def check_locomotive(self, locomotive: Locomotive):
        if locomotive.check_state():
            print("The locomotive is working correctly")
        else:
            print("The locomotive has to be serviced")
            self.__service_locomotive(locomotive)






