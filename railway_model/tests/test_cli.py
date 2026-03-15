import pytest
import sys
from cli.cli import Cli
from management.serializer import Serializer
from management.passenger_serializer import PassengerSerializer
from cli.timer import Timer
from cli.parser import Parser


@pytest.fixture()
def parser():
    return Parser.build_parser()


def test_state(parser):
    args = parser.parse_args((["state", "1"]))
    assert args.command == "state"
    assert args.state_id == 1


@pytest.fixture(autouse=True)
def temp_files(tmp_path, monkeypatch):
    monkeypatch.setattr(Serializer, "STATE_FILE", str(tmp_path / "state.json"))
    monkeypatch.setattr(PassengerSerializer, "PASSENGERS_FILE", str(tmp_path / "passengers.json"))
    monkeypatch.setattr(Timer, "TIME_FILE", str(tmp_path / "time.json"))


def run_cli(*args):
    sys.argv = ["railway-cli"] + list(args)
    return Cli.cli()


def test_cli_timetable():
    result = run_cli("timetable")
    assert result == 0


def test_cli_create_and_state():
    run_cli("compound", "1", "2", "A")
    result = run_cli("state", "1")
    assert result == 0


def test_cli_create_passenger():
    result = run_cli("passenger", "Passenger", "500")
    assert result == 0


def test_cli_book_passenger_not_found():
    run_cli("compound", "1", "2", "A")
    result = run_cli("book", "1", "1", "1", "999")
    assert result == 1


def test_cli_state_compound_not_found():
    result = run_cli("state", "999")
    assert result == 1


def test_now():
    result = run_cli("now")
    assert result == 0

