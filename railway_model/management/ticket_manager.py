from passenger.passenger import Passenger
from passenger.ticket import Ticket
from compound.compound import Compound, Coach
from exceptions.exceptions import TicketSellingError


class TicketManager:

    @staticmethod
    def create_ticket(passenger: Passenger, compound: Compound,
                      coach: Coach, seat_number: int, time: int):
        if coach.seat_price > passenger.finance:
            raise TicketSellingError("Not enough funds")
        if seat_number not in coach.seats.keys():
            raise TicketSellingError("Wrong seat number")
        if coach not in compound.coaches:
            raise TicketSellingError("Wrong coach")
        coach.occupy_seat(seat_number, passenger.passenger_id)
        ticket = Ticket(compound, coach, seat_number, time)
        passenger.get_ticket(ticket)
        passenger.change_finance(-coach.seat_price)
