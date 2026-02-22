from enum import Enum


class TrainState(Enum):
    AT_STATION = "at_station"
    MOVING = "moving"
    STOPPED = "stopped"


