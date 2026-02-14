from compound.compound import Compound, Coach


class Ticket:
    def __init__(self, compound: Compound, coach: Coach, seat_number: int,  time: int):
        self.compound = compound
        self.time = time
        self.coach = coach
        self.seat_number = seat_number

    def __str__(self):
        return f"Race {self.compound.compound_id}, {self.time}"