import pytest
from compound.coach import Coach
from compound.locomotive import Locomotive
from compound.compound import Compound
from exceptions.exceptions import SeatError


def test_coach():
    number = 11
    seat_amount = 5
    seat_price = 26
    coach = Coach(number, seat_amount, seat_price)
    assert coach.number == 11
    assert coach.seat_price == 26
    assert coach.seats == {1: None, 2: None, 3: None, 4: None, 5: None}
    coach.occupy_seat(3, 90)
    assert coach.seats == {1: None, 2: None, 3: 90, 4: None, 5: None}
    coach.free_seat(3)
    assert coach.seats == {1: None, 2: None, 3: None, 4: None, 5: None}
    with pytest.raises(SeatError):
        coach.free_seat(1)
        coach.occupy_seat(99, 99)


def test_locomotive():
    locomotive = Locomotive(34)
    assert locomotive.number == 34


def test_compound():
    locomotive = Locomotive(34)
    compound = Compound(locomotive, [])
    coach1 = Coach(1, 5, 26)
    coach2 = Coach(2, 6, 37)
    compound.add_coach(coach2)
    compound.add_coach(coach1)
    assert compound.coaches == [coach1, coach2]


