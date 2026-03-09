import json
from typing import Dict
from passenger.passenger import Passenger
from pathlib import Path
from exceptions.exceptions import TimetableError
from management.ticket_manager import TicketManager
from management.timetable import Timetable
from passenger.ticket import Ticket


class PassengerSerializer:
    PASSENGERS_FILE = "data/passengers.json"

    @staticmethod
    def load_passengers(path=PASSENGERS_FILE) -> dict:
        if not Path(path).exists():
            return {"id_counter": 1, "passengers": {}}
        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def save_passenger(passenger: Passenger, path=PASSENGERS_FILE):
        data = PassengerSerializer.load_passengers(path)
        data["passengers"][str(passenger.passenger_id)] = {
            "passenger_id": passenger.passenger_id,
            "name": passenger.name,
            "finance": passenger.finance,
            "tickets": [
                {
                    "compound_id": t.compound.compound_id,
                    "coach_number": t.coach.number,
                    "seat_number": t.seat_number,
                    "time": t.time
                } for t in passenger.tickets
            ]
        }
        data["id_counter"] = Passenger.id_counter
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def get_passenger(passenger_id: int, timetable: Timetable, path=PASSENGERS_FILE):
        data = PassengerSerializer.load_passengers(path)
        pass_data = data.get("passengers", {}).get(str(passenger_id))
        if not pass_data:
            raise TimetableError(f"Passenger {passenger_id} not found")
        Passenger.id_counter = data.get("id_counter", 1)
        passenger = Passenger.__new__(Passenger)
        passenger._Passenger__passenger_id = pass_data["passenger_id"]
        passenger._Passenger__name = pass_data["name"]
        passenger._Passenger__finance = pass_data["finance"]
        passenger._Passenger__tickets = []
        compounds = {cell.compound.compound_id:cell.compound for cell in timetable.cells}
        for ticket in pass_data.get("tickets", []):
            compound = compounds.get(ticket["compound_id"])
            if compound:
                coach = next((coach for coach in compound.coaches if coach.number == ticket["coach_number"]), None)
                if coach:
                    ticket = Ticket(compound, coach, ticket["seat_number"], ticket["time"])
                    passenger._Passenger__tickets.append(ticket)
        return passenger

    @staticmethod
    def remove_tickets_for_compound(compound_id: int, path=PASSENGERS_FILE):
        data = PassengerSerializer.load_passengers(path)
        for pass_data in data.get("passengers", {}).values():
            pass_data["tickets"] = [
                t for t in pass_data.get("tickets", [])
                if t["compound_id"] != compound_id
            ]
        with open(path, "w") as file:
            json.dump(data, file, indent=2)
