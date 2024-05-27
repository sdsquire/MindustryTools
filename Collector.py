from MindustryObject import Building
from Material import Material

from typing import Dict

class Collector(Building):
    def __init__(self, 
                id: str,
                name: str,
                power: int,
                size: int, 
                outputs: Dict[Material, float],
                ):
        super().__init__(id, name, power, size, {}, outputs)

class Drill(Collector):
    def __init__(self, 
                id: str,
                name: str,
                power: int,
                size: int, 
                output: Material,
                ):
        super().__init__(id, name, power, size, {}, {output: 1.0})

class Pump(Collector):
    def __init__(self, 
                id: str,
                name: str,
                power: int,
                size: int, 
                output: Material,
                ):
        super().__init__(id, name, power, size, {output: 1.0})