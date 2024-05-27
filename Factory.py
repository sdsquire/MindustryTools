from typing import Dict

from MindustryObject import Building
from Material import Material

class Factory(Building):
    def __init__(self,
                 id: str,
                name: str,
                power: int,
                size: int,
                inputs: Dict[Material, float],
                outputs: Dict[Material, float],
                ):
        super().__init__(id, name, power, size)
        self.inputs = inputs
        self.outputs = outputs

    def __repr__(self):
        return self.name
    
