from dataclasses import dataclass

@dataclass
class MindustryObject:
    '''
    The base for all mindustry objects.

    Attributes:
        id (str): The id of the object, as given by the keyboard shortcuts in-game (no leading zeros)
        name (str): The object name
    '''
    id: str
    name: str

@dataclass
class Building(MindustryObject):
    '''
    The base for any Mindustry building. This includes collectors, factories, and power generators.    

    Attributes:
        power (int): The amount of power the building consumes.
        size (int): The size of the building, given as the length of one side (all buildings are square).
    '''
    power: int
    size: int 

    def __hash__(self):
        return self.id

class MindustryException(Exception):
    '''
    An exception thrown when game rules are violated.
    '''
    def __init__(self, message):
        super().__init__(message)