class MindustryObject:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return isinstance(other, MindustryObject) and self.id == other.id

    def __repr__(self):
        return self.name
    
class Building(MindustryObject):
    def __init__(self, 
                id: str,
                name: str,
                power: int,
                size: int, 
                ):
        super().__init__(id, name)
        self.power = power
        self.size = size
        self.efficiency = 1.0
