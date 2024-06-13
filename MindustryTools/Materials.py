from dataclasses import dataclass, field
from typing import List

from .MindustryObject import MindustryObject, Building

@dataclass(frozen=True)
class Material(MindustryObject):
    '''
    Represents a mindustry material. Materials include items, liquids, and power.

    Args:
        id (str): The id of the material.
        name (str): The name of the material.
        hardness (Optional[int]): The hardness of the material.
        is_liquid (bool, optional): Whether the material is a liquid. Defaults to False.
        is_natural (bool, optional): Whether the material can be found to mine. Defaults to False.

    Other Attributes:
        sources (List[Building]): The buildings that produce this material.
        source (Building): The buildling of choice that produces this material. Can be modified.
    '''
    hardness: int = None
    is_liquid: bool = False
    is_natural: bool = False
    sources: List[Building] = field(default_factory=list)
    source: Building = None

    # def set_source(self, source: Building) -> None:
    #     '''
    #     Set the preferred source of the material.

    #     Args:
    #         source (Building): The building that produces the material.
    #     '''
    #     if source not in self.sources:
    #         self.sources.append(source)
    #     self.source = source
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Material) and self.id == other.id

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

POWER = Material(name='Power', id=0)
COPPER = Material(name='Copper', id=1, hardness=1, is_natural=True)
LEAD = Material(name='Lead', id=1, hardness=1, is_natural=True)
GRAPHITE = Material(name='Graphite', id=2)
SILICON = Material(name='Silicon', id=3)
COAL = Material(name='Coal', id=4, hardness=2, is_natural=True)
SAND = Material(name='Sand', id=5, hardness=0, is_natural=True)
METAGLASS = Material(name='Metaglass', id=6)
TITANIUM = Material(name='Titanium', id=7, hardness=3, is_natural=True)
PLASTANIUM = Material(name='Plastanium', id=8)
THORIUM = Material(name='Thorium', id=9, hardness=4, is_natural=True)
PHASE_FABRIC = Material(name='Phase_fabric', id=10)
SURGE_ALLOY = Material(name='Surge_alloy', id=11)
SCRAP = Material(name='Scrap', id=12, hardness=0, is_natural=True)
SPORE_POD = Material(name='Spore_pod', id=13)
PYRATITE = Material(name='Pyratite', id=14)
BLAST_COMPOUND = Material(name='Blast_compound', id=15)

WATER = Material(name='Water', id=16, is_liquid=True, is_natural=True)
SLAG = Material(name='Slag', id=17, is_liquid=True)
OIL = Material(name='Oil', id=18, is_liquid=True, is_natural=True)
CRYOFLUID = Material(name='Cryofluid', id=19, is_liquid=True)

MATERIALS = [COPPER, LEAD, GRAPHITE, SILICON, COAL, SAND, METAGLASS, TITANIUM, PLASTANIUM, THORIUM, PHASE_FABRIC, SURGE_ALLOY, SCRAP, SPORE_POD, PYRATITE, BLAST_COMPOUND, WATER, SLAG, OIL, CRYOFLUID]