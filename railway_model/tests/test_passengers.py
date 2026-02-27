import pytest
from exceptions.exceptions import TicketSellingError
from passenger.passenger import Passenger, Ticket
from compound.compound import Compound, Locomotive, Coach
from management.ticket_manager import TicketManager
from management.timetable_manager import TimetableManager, TimetableCell, Timetable, TimetableError
from railway.route import Route, Station, Railway


def test_passenger():
    passenger = Passenger("name", 100)
    locomotive = Locomotive(34)
    compound = Compound(locomotive, [])
    coach1 = Coach(1, 5, 26)
    coach2 = Coach(2, 6, 37)
    compound.add_coach(coach2)
    compound.add_coach(coach1)
    TicketManager.create_ticket(passenger, compound, coach2, 2, 800)
    assert passenger.tickets[0].coach == coach2
    assert passenger.tickets[0].time == 800
    assert passenger.tickets[0].compound == compound
    assert passenger.finance == 63
    TicketManager.create_ticket(passenger, compound, coach2, 3, 800)
    with pytest.raises(TicketSellingError):
        TicketManager.create_ticket(passenger, compound, coach2, -1, 800)
        TicketManager.create_ticket(passenger, compound, coach2, 4, 800)


def test_timetable():
    locomotive = Locomotive(35)
    compound = Compound(locomotive, [])
    coach1 = Coach(1, 5, 26)
    coach2 = Coach(2, 6, 37)
    compound.add_coach(coach2)
    compound.add_coach(coach1)
    stations = {Station("A"), Station("B")}
    route = Route([Railway(stations, 100)])
    cell = TimetableCell(compound, route, 900)
    assert cell.route == route
    timetable = Timetable()
    TimetableManager.add_cell(timetable, cell)
    cell2 = TimetableCell(compound, route, 700)
    TimetableManager.add_cell(timetable, cell2)
    assert timetable.cells == [cell2, cell]
    TimetableManager.remove_cell(timetable, cell)
    assert timetable.cells == [cell2]
    with pytest.raises(TimetableError):
        TimetableManager.remove_cell(timetable, cell)
