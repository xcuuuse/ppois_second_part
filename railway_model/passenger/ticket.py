from compound.compound import Compound


class Ticket:
    def __init__(self, compound: Compound, time: int):
        self.compound = compound
        self.time = time

    def __str__(self):
        return f"Race {self.compound.compound_id}, {self.time}"