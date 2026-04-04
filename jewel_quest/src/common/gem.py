import random
from enum import Enum


class GemType(Enum):
    RUBY = ((220, 40, 60), (255, 120, 130))
    SAPPHIRE = ((40, 80, 220), (100, 160, 255))
    EMERALD = ((40, 190, 80), (120, 255, 140))
    TOPAZ = ((220, 170, 30), (255, 220, 80))
    AMETHYST = ((160, 50, 220), (210, 130, 255))
    DIAMOND = ((180, 220, 240), (240, 250, 255))

    def __init__(self, color, shine):
        self.color = color
        self.shine = shine

    @staticmethod
    def random():
        return random.choice(list(GemType))

