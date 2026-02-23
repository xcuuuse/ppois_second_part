from typing import List
from management.validator import Validator
from .ticket import Ticket


class Passenger:
    _id_counter = 1

    def __init__(self, name: str, finance: int):
        Validator.validate(locals(), {
            "name": (str, lambda s: s != ""),
            "finance": (int, lambda x: x >= 0)
        })
        self.__passenger_id = Passenger._id_counter
        Passenger._id_counter += 1
        self.__name = name
        self.__tickets: List[Ticket] = []
        self.__finance = finance

    @property
    def passenger_id(self):
        return self.__passenger_id

    @property
    def tickets(self):
        return self.__tickets

    @property
    def finance(self):
        return self.__finance

    def get_ticket(self, ticket: Ticket):
        self.__tickets.append(ticket)
        self.__tickets.sort(key=lambda t: t.time)

    def change_finance(self, amount: int):
        self.__finance += amount

