import json
from pathlib import Path
from compound.compound import Compound
from compound.locomotive import Locomotive
from compound.coach import Coach
from enums.enums import TrainState
from management.timetable import Timetable, TimetableCell
from railway.route import Station, Railway, Route


class Serializer:
    STATE_FILE = "state.json"

    @staticmethod
    def save(timetable: Timetable, path=STATE_FILE):
        compounds_data = []
        for cell in timetable.cells:
            compound = cell.compound
            data = {
                "compound_id": compound.compound_id,
                "locomotive": {
                    "number": compound.locomotive.number,
                    "usage_count": compound.locomotive.usage_count,
                    "is_usable": compound.locomotive.is_usable,
                    "min_damage": compound.locomotive.minimum_damage_level,
                    "max_damage": compound.locomotive.maximum_damage_level
                },
                "coaches": [{
                    "number": coach.number,
                    "seats_amount": len(coach.seats),
                    "seat_price": coach.seat_price,
                    "seats": {str(k): v for k, v in coach.seats.items()}
                } for coach in compound.coaches],
                "current_pos": compound.current_pos,
                "state": compound.state.value
            }
            compounds_data.append(data)
        timetable_data = []
        for cell in timetable.cells:
            station_names = [station.name for station in cell.route.stations]
            timetable_data.append(
                {
                    "compound_id": cell.compound.compound_id,
                    "route": station_names,
                    "time": cell.time
                }
            )
        data = {
            "global_state": {  # ✅ ПРАВИЛЬНО: на верхнем уровне
                "compound_id_counter": Compound._Compound__compound_id_counter
            },
            "compounds": compounds_data,
            "timetable": timetable_data
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load(path=STATE_FILE):
        if not Path(path).exists():
            raise FileNotFoundError("State file not found")

        with open(path, "r") as f:
            data = json.load(f)
        Compound._Compound__compound_id_counter = data["global_state"]["compound_id_counter"]
        compounds = {}
        for c_data in data["compounds"]:
            locomotive_data = c_data["locomotive"]
            locomotive = Locomotive(locomotive_data["number"])
            locomotive.usage_count = locomotive_data["usage_count"]
            locomotive.is_usable = locomotive_data["is_usable"]
            locomotive.minimum_damage_level = locomotive_data["min_damage"]
            locomotive.maximum_damage_level = locomotive_data["max_damage"]

            coaches = []
            for coach_data in c_data["coaches"]:
                coach = Coach(coach_data["number"], coach_data["seats_amount"], coach_data["seat_price"])
                for seat, pid in coach_data["seats"].items():
                    if pid is not None:
                        coach.occupy_seat(int(seat), pid)
                coaches.append(coach)

            compound = Compound(locomotive, coaches, c_data["compound_id"])
            compound._Compound__current_pos = c_data["current_pos"]
            compound.state = TrainState(c_data["state"])
            compounds[c_data["compound_id"]] = compound

        timetable = Timetable()
        for t_data in data["timetable"]:
            stations = [Station(name) for name in t_data["route"]]
            railways = []
            for i in range(len(stations) - 1):
                railways.append(Railway({stations[i], stations[i + 1]}, 100))
            route = Route(railways)

            compound = compounds[t_data["compound_id"]]

            cell = TimetableCell(compound, route, t_data["time"])
            timetable.cells.append(cell)
        return timetable
