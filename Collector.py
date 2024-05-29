from MindustryObject import Building
from Material import Material

from typing import Dict

class Collector(Building):
    def __init__(self, 
                id: str,
                name: str,
                power: int,
                size: int,
                base_speed: float,
                ):
        super().__init__(id, name, power, size)
        self.base_speed = base_speed

class Drill(Collector):
    def __init__(self, 
                id: str,
                name: str,
                power: int,
                size: int, 
                base_speed: float,
                max_hardness: int,
                water_intake: float,
                water_boosted = False,
                boost_multiplier = 2.56,
                ):
        super().__init__(id, name, power, size)

class Pump(Collector):
    def __init__(self, 
                id: str,
                name: str,
                power: int,
                size: int, 
                output: Material,
                base_speed: float,
                ):
        super().__init__(id, name, power, size, {output: 1.0})