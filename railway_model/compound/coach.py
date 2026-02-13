from exceptions.exceptions import SeatError


class Coach:
    def __init__(self, number: int, seats_amount: int, seat_price: int):
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

    def occupy_seat(self, number: int, pass_id: int):
        if number not in self.__seats.keys():
            raise SeatError("Incorrect seat number")
        self.__seats[number] = pass_id

    def free_seat(self, number: int):
        if number not in self.__seats.keys() or self.__seats[number] is None:
            raise SeatError("Incorrect seat number to free")
        self.__seats[number] = None




