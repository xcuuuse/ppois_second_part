import pytest
import json
import os
from pathlib import Path
from compound.compound import Compound
from compound.locomotive import Locomotive
from compound.coach import Coach
from enums.enums import TrainState
from management.timetable import Timetable, TimetableCell
from railway.route import Station, Railway, Route
from management.serializer import Serializer
from passenger.passenger import Passenger
from management.ticket_manager import TicketManager


@pytest.fixture
def temp_state_file(tmp_path):
    file_path = tmp_path / "test_state.json"
    yield str(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture
def sample_compound():
    locomotive = Locomotive(1)
    coaches = [
        Coach(1, 5, 25),
        Coach(2, 4, 45)
    ]
    return Compound(locomotive, coaches)


@pytest.fixture
def sample_timetable(sample_compound, sample_route):
    timetable = Timetable()
    timetable.cells.append(TimetableCell(sample_compound, sample_route, 800))
    return timetable


@pytest.fixture
def sample_route():
    return Route([
        Railway({Station("A"), Station("B")}, 100),
        Railway({Station("B"), Station("C")}, 100),
        Railway({Station("C"), Station("D")}, 100)
    ])


def test_serializer(temp_state_file, sample_timetable):
    Serializer.save(sample_timetable, temp_state_file)
    assert os.path.exists(temp_state_file)
    loaded_timetable = Serializer.load(temp_state_file)
    assert len(loaded_timetable.cells) == 1
    loaded_cell = loaded_timetable.cells[0]
    original_cell = sample_timetable.cells[0]
    assert loaded_cell.compound.compound_id == original_cell.compound.compound_id
    assert len(loaded_cell.compound.coaches) == len(original_cell.compound.coaches)
    assert loaded_cell.compound.current_pos == original_cell.compound.current_pos
    assert loaded_cell.compound.state == original_cell.compound.state
    assert loaded_cell.time == original_cell.time
