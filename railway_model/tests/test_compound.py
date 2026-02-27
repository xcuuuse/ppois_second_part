import pytest
from compound.coach import Coach
from compound.compound import Compound, TrainState, Route, Station
from exceptions.exceptions import SeatError
from exceptions.exceptions import CreatingEntityError
from management.locomotive_manager import LocomotiveManager, Locomotive
from railway.railway import Railway


def test_coach():
    number = 11
    seat_amount = 5
    seat_price = 26
    wrong_num = '11'
    wrong_price = '26'
    coach = Coach(number, seat_amount, seat_price)
    with pytest.raises(CreatingEntityError):
        wrong_coach = Coach(wrong_num, seat_amount, wrong_price)
    coach.occupy_seat(1, 9)
    assert coach.free_seats == [2, 3, 4, 5]
    coach.free_seat(1)
    assert coach.free_seats == [1, 2, 3, 4, 5]
    coach.occupy_seat(1, 5)
    coach.occupy_seat(2, 4)
    coach.occupy_seat(3, 6)
    with pytest.raises(SeatError):
        coach.occupy_seat('a', 5)
    assert coach.free_seats == [4, 5]
    coach.free_coach()
    assert coach.free_seats == [1, 2, 3, 4, 5]

def test_locomotive():
    locomotive = Locomotive(34)
    with pytest.raises(CreatingEntityError):
        wrong_locomotive = Locomotive(-1)
        wrong_locomotive2 = Locomotive('abc')
    manager = LocomotiveManager()
    manager.add_locomotive(locomotive)
    manager.check_locomotive(locomotive)
    manager.add_locomotive(locomotive)
    assert locomotive.is_usable
    locomotive.start_engine()
    assert locomotive.usage_count == 1


def test_compound():
    locomotive = Locomotive(34)
    compound = Compound(locomotive, [])
    coach1 = Coach(1, 5, 26)
    coach2 = Coach(2, 6, 37)
    compound.add_coach(coach2)
    compound.add_coach(coach1)
    assert compound.coaches == [coach1, coach2]
    assert compound.state == TrainState.STOPPED
    route = Route([Railway({Station("A"), Station("B")}, 100)])
    compound.move_along_route(route)
    assert compound.state == TrainState.AT_STATION
    compound.process_station_actions()
    assert compound.state == TrainState.AT_STATION




