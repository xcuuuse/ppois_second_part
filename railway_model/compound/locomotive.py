import random
from exceptions.exceptions import LocomotiveUsingError


class Locomotive:
    def __init__(self, number: int):
        self.number = number
        self.__usage_count = 0
        self.__is_usable = True
        self.__minimum_damage_level = 0.01
        self.__maximum_damage_level = 0.3

    def check_state(self):
        if self.__is_usable:
            prob = min(self.__minimum_damage_level + self.__usage_count*0.01, self.__maximum_damage_level)
            if random.random() < prob:
                self.__is_usable = False

    def start_engine(self):
        self.check_state()
        if not self.__is_usable:
            raise LocomotiveUsingError("The locomotive is broken")
        self.__usage_count += 1

    def get_service(self):
        self.__usage_count = 0
        self.__is_usable = True



