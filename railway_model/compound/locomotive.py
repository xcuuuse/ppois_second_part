import random
from exceptions.exceptions import LocomotiveUsingError
from management.validator import Validator


class Locomotive:
    def __init__(self, number: int):
        Validator.validate(locals(), {"number": (int, lambda x: x >= 0)})
        self.number = number
        self.usage_count = 0
        self.is_usable = True
        self.minimum_damage_level = 0.01
        self.maximum_damage_level = 0.3

    def check_state(self):
        if self.is_usable:
            prob = min(self.minimum_damage_level + self.usage_count*0.01, self.maximum_damage_level)
            if random.random() < prob:
                self.is_usable = False

    def start_engine(self):
        self.check_state()
        if not self.is_usable:
            raise LocomotiveUsingError("The locomotive is broken")
        self.usage_count += 1



    def get_service(self):
        self.usage_count = 0
        self.is_usable = True




