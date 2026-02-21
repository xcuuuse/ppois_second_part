from compound.compound import Compound
from railway.route import Route


class TimetableCell:
    def __init__(self, compound: Compound, route: Route, time: int):
        self.compound = compound
        self.route = route
        self.time = time

    def __str__(self):
        return (f"The train {self.compound.compound_id}"
                f"({self.route.stations[0]} - {self.route.stations[-1]}) departs at {self.time}.")

    def __eq__(self, other):
        if isinstance(other, TimetableCell):
            return (self.compound == other.compound
                    and self.route == other.route
                    and self.time == other.time)
        return False

    def __hash__(self):
        return hash((self.compound, self.route, self.time))