from .ticket import Ticket

class Passenger:
    _id_counter = 1

    def __init__(self, name: str, finance: int, tickets: list[Ticket]):
        self.__passenger_id = Passenger._id_counter
        Passenger._id_counter += 1
        self.__name = name
        self.__tickets = tickets

    @property
    def passenger_id(self):
        return self.__passenger_id

    @property
    def tickets(self):
        return self.__tickets

    def get_ticket(self, ticket: Ticket):
        self.__tickets.append(ticket)
