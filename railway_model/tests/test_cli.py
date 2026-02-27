import pytest
import sys
import os
from pathlib import Path
from management.serializer import Serializer
from compound.compound import Compound
from compound.locomotive import Locomotive
from compound.coach import Coach
from railway.route import Route, Railway, Station
from management.timetable import Timetable, TimetableCell
from cli.cli import Cli, Timer


def test_state(tmp_path, capsys):
    state_file = tmp_path / "test_state.json"
    Serializer.STATE_FILE = str(state_file)
    Timer.TIME_FILE = str(tmp_path / "time.json")
    station_O = Station("O")
    station_A = Station("A")
    locomotive = Locomotive(1)
    coaches = [Coach(1, 5, 25), Coach(2, 4, 45)]
    compound = Compound(locomotive, coaches)
    route = Route([Railway({station_O, station_A}, 100)
    ])
    timetable = Timetable()
    timetable.cells.append(TimetableCell(compound, route, 800))
    Serializer.save(timetable, str(state_file))
    sys.argv = ["railway-cli", "state", "1"]
    result = Cli.cli()

    assert result == 0

    captured = capsys.readouterr()
    output = captured.out

    assert "Current state" in output
    assert "Compound ID: 1" in output
    assert "Pos: 0 (A)" in output
    assert "State: STOPPED" in output
    assert "Coach 1 (price: 25): 5/5 free seats" in output
    assert "Coach 2 (price: 45): 4/4 free seats" in output
