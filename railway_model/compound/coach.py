from exceptions.exceptions import SeatError
from management.validator import Validator



class Coach:
    def __init__(self, number: int, seats_amount: int, seat_price: int):
        Validator.validate(locals(), {
            "number": (int, lambda x: x >= 0),
            "seats_amount": (int, lambda x: x > 0),
            "seat_price": (int, lambda x: x > 0)
        })
        self.__number = number
        self.__seat_price = seat_price
        self.__seats: dict = {}
        for seat in range(1, seats_amount + 1):
            self.__seats[seat] = None

    @property
    def number(self):
        return self.__number

    @property
    def seats(self):
        return self.__seats

    @property
    def seat_price(self):
        return self.__seat_price

    @property
    def free_seats(self):
        return [i for i in self.__seats.keys() if self.__seats[i] is None]

    def occupy_seat(self, number: int, pass_id: int):
        if number not in self.__seats.keys() or self.__seats[number] is not None:
            raise SeatError("The seat number is wrong or the seat is occupied")
        self.__seats[number] = pass_id

    def free_seat(self, number: int):
        if number not in self.__seats.keys() or self.__seats[number] is None:
            raise SeatError("Incorrect seat number to free")
        self.__seats[number] = None

    def free_coach(self):
        for i in self.__seats:
            self.free_seat(i)


