import json
from pathlib import Path
from compound.compound import Compound
from compound.locomotive import Locomotive
from compound.coach import Coach
from enums.enums import TrainState


class Serializer:
    @staticmethod
    def save(compound: Compound, path="train_state.json"):
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
                "seats": {str(k): v for k, v in coach.seats.items()}
            } for coach in compound.coaches],
            "current_pos": compound.current_pos,
            "state": compound.state.value
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def load(path="train_state.json"):
        if not Path(path).exists():
            raise FileNotFoundError("State file not found")

        with open(path, "r") as f:
            data = json.load(f)

        locomotive = Locomotive(data["locomotive"]["number"])
        locomotive.usage_count = data["locomotive"]["usage_count"]
        locomotive.is_usable = data["locomotive"]["is_usable"]
        locomotive.minimum_damage_level = data["locomotive"]["min_damage"]
        locomotive.maximum_damage_level = data["locomotive"]["max_damage"]

        coaches = []
        for c_data in data["coaches"]:
            coach = Coach(c_data["number"], c_data["seats_amount"], c_data["seat_price"])
            for seat, pid in c_data["seats"].items():
                if pid is not None:
                    coach.occupy_seat(int(seat), pid)
            coaches.append(coach)

        compound = Compound(locomotive, coaches, data["compound_id"])
        compound._Compound__current_pos = data["current_pos"]
        compound.state = TrainState(data["state"])
        return compound

