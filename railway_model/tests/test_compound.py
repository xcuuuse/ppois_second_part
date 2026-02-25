import pytest
from compound.coach import Coach
from compound.locomotive import Locomotive
from compound.compound import Compound
from exceptions.exceptions import SeatError
from exceptions.exceptions import CreatingEntityError

def test_coach():
    number = 11
    seat_amount = 5
    seat_price = 26
    wrong_num = '11'
    wrong_amount = '5'
    wrong_price = '26'
    coach = Coach(number, seat_amount, seat_price)
    with pytest.raises(CreatingEntityError):
        wrong_coach = Coach(wrong_num, seat_amount, wrong_price)
    coach.occupy_seat(1, 9)
    assert coach.free_seats == [2, 3, 4, 5]
    coach.free_seat(1)
    assert coach.free_seats == [1, 2, 3, 4, 5]
    coach.occupy_seat(1, 5)
    with pytest.raises(SeatError):
        coach.occupy_seat('a', 5)
        coach.occupy_seat(0, 4)
        coach.occupy_seat(1, 6)
        coach.free_seat(8)


def test_locomotive():
    locomotive = Locomotive(34)
    with pytest.raises(CreatingEntityError):
        wrong_locomotive = Locomotive(-1)
        wrong_locomotive2 = Locomotive('abc')




def test_compound():
    locomotive = Locomotive(34)
    compound = Compound(locomotive, [])
    coach1 = Coach(1, 5, 26)
    coach2 = Coach(2, 6, 37)
    compound.add_coach(coach2)
    compound.add_coach(coach1)
    assert compound.coaches == [coach1, coach2]


