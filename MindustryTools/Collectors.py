from dataclasses import dataclass
from typing import Optional

from MindustryTools.MindustryObject import Building, MindustryException
from MindustryTools.Materials import Material

@dataclass(frozen=True)
class Collector(Building):
    '''
    Represents a mindustry collector. Collectors gateher resources from the environment, and have no required inputs except power.
    Note that some buildings that are identified as collectors in-game function more like factories, and are represented as such.

    Args:
        id (str): The id of the collector, as given by the keyboard shortcuts in-game (no leading zeros).
        name (str): The name of the collector.
        power (int): The amount of power the collector consumes.
        size (int): The size of the collector, given as the length of one side (all collectors are square).
        base_speed (float): The base speed of the collector per tile.
    '''
    base_speed: float

    def get_speed(self, material: Material, tiles: Optional[int]=None) -> float:
        '''
        Get the speed of the collector.

        Args:
            material (Material): The material the collector is collecting.
            tiles (int, optional): The number of tiles the collector is collecting from. Defaults to full coverage.

        Returns:
            float: The speed of the collector.
        '''
        if not material.is_natural:
            raise MindustryException(f"{material.name} is not a natural resource.")
        if tiles is None:
            tiles = self.size**2
        return self.base_speed * tiles

    def required_tiles(self, material: Material, target_rate: float) -> float:
        '''
        Get the number of tiles required to achieve a target collection rate.

        Args:
            target_rate (float): The target collection rate.

        Returns:
            int: The number of tiles required.
        '''
        return target_rate / self.get_speed(material, tiles=1)


@dataclass(frozen=True)
class Drill(Collector):
    '''
    Represents a mindustry drill. Drills are collectors that gather materials from ore deposits.

    Args:
        id (str): The id of the drill, as given by the keyboard shortcuts in-game (no leading zeros).
        name (str): The name of the drill.
        power (int): The amount of power the drill consumes.
        size (int): The size of the drill, given as the length of one side (all drills are square).
        output (Material): The material the drill produces.
        base_speed (float): The base speed of the drill per tile.
        max_hardness (int): The maximum material hardness the drill can mine.
        boosted (bool): Whether the drill is boosted.
        water_intake (float): The amount of water the drill consumes per second when boosted.
        boost_multiplier (float): The multiplier for the drill's speed when boosted by water.
    '''
    max_hardness: int
    water_intake: float 
    boost_multiplier: float = 2.56
    boosted: bool = False

    def get_speed(self, material, tiles=None) -> float:
        '''
        Get the speed of the drill.

        Returns:
            float: The speed of the drill.
        '''
        if tiles is None:
            tiles = self.size**2
        if material.hardness > self.max_hardness:
            raise MindustryException(f"{material.name} is too hard for this drill.")

        return (60 / (self.base_speed + (50 * material.hardness))) * tiles * (self.water_boost if self.boosted else 1)


@dataclass(frozen=True)
class Pump(Collector):
    def get_speed(self, material, tiles: Optional[int]=None) -> float:
        '''
        Get the speed of the pump.

        Args:
            material (Material): The liquid the pump is collecting. Defaults to water.
            tiles (int, optional): The number of tiles the pump is collecting from. Defaults to full coverage.
        '''
        if not material.is_liquid:
            raise MindustryException(f"{material.name} is not a liquid.")
        return super().get_speed(material=material, tiles=tiles)
    

# DRILLS
@dataclass(frozen=True)
class MechanicalDrill(Drill):
    id: int = 201
    name: str = 'Mechanical Drill'
    power: int = 0
    size: int = 2
    max_hardness: int = 2
    base_speed: float = 600.0
    water_intake: float = 3.0

@dataclass(frozen=True)
class PneumaticDrill(Drill):
    id: int = 202
    name: str = 'Pneumatic Drill'
    power: int = 0
    size: int = 2
    max_hardness: int = 3
    base_speed: float = 400.0
    water_intake: float = 3.6

@dataclass(frozen=True)
class LaserDrill(Drill):
    id: int = 203
    name: str = 'Laser Drill'
    power: int = -60
    size: int = 3
    max_hardness: int = 4
    base_speed: float = 280.0
    water_intake: float = 4.8

@dataclass(frozen=True)
class AirblastDrill(Drill):
    id: int = 204
    name: str = 'Airblast Drill'
    power: int = -60
    size: int = 4
    max_hardness: int = 4
    base_speed: float = 280.0
    water_intake: int = 3
    water_boost: float = 3.24

#PUMPS
@dataclass(frozen=True)
class MechanicalPump(Pump):
    id: int = 401
    name: str = 'Mechanical Pump'
    power: int = 0
    size: int = 1
    base_speed: float = 7.0

@dataclass(frozen=True)
class RotaryPump(Pump):
    id: int = 402
    name:str = 'Rotary Pump'
    power: int = -18
    size: int = 2
    base_speed: float = 12.2

@dataclass(frozen=True)
class ImpulsePump(Pump):
    id: int = 403
    name: str = 'Impulse Pump'
    power: int = -78
    size: int = 3
    base_speed: float = 13.2

DRILLS = {collector.id: collector for collector in [MechanicalDrill(), PneumaticDrill(), LaserDrill(), AirblastDrill()]}
PUMPS = {collector.id: collector for collector in [MechanicalPump(), RotaryPump(), ImpulsePump()]}
