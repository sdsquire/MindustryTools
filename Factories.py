from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List
from math import ceil

from MindustryObject import Building, MindustryObject
import Materials as M

@dataclass
class Factory(Building):
    '''
    A factory building in Mindustry. This includes all buildings that take inputs and produce outputs.
    Note that this includes some things that are not classified as factories in-game, such as power generators and water extractors.
    '''
    inputs: Dict[M.Material, float] = None
    outputs: Dict[M.Material, float] = None
    efficiency: float = 1.0

    def __post_init__(self):
        self.power = self.power * self.efficiency
        self.inputs =  {material: self.efficiency * rate for material, rate in self.inputs.items()}
        for material, rate in self.outputs.items():
            self.outputs[material] = self.efficiency * rate
            material.set_source(self)
        
    def __hash__(self):
        return self.id
    
    def __eq__(self, other):
        if isinstance(other, Factory):
            return self.id == other.id
    
    def __eq__(self, other):
        return isinstance(other, Factory) and self.id == other.id
    
    def __add__(self, other):
        return FactoryGroup([self]).__add__(other)

    def __radd__(self, other):
        return FactoryGroup([self]).__radd__(other)

    def __sub__(self, other):
        return FactoryGroup([self]).__sub__(other)

    def __rsub__(self, other):
        return FactoryGroup([self]).__rsub__(other)
  
    def __mul__(self, other):
        return FactoryGroup([self]).__mul__(other)
        
    def __rmul__(self, other):
        return FactoryGroup([self]).__rmul__(other)

    def __matmul__(self, other):
        return FactoryGroup([self]).__matmul__(other)
    
    def __truediv__(self, other):
        return FactoryGroup([self]).__truediv__(other)

class FactoryGroup():
    'This treats a group of factories as a single entity.'
    def __init__(self, factories: List[Factory] = None, *, rounded = False, materials: Optional[List[M.Material]] = None, factory_group: Optional['FactoryGroup'] = None):
        self.rounded = rounded
        self.factories = factory_group.factories.copy() if factory_group is not None else dict()
        self.IOMap = factory_group.IOMap.copy() if factory_group is not None else dict()
        if factories is not None:
            for factory in factories: # Combine inputs and outputs of all factories
                self.factories[factory] = self.factories.get(factory, 0) + 1
                for material, rate in factory.outputs.items():
                    self.IOMap[material] = self.IOMap.get(material, 0) + rate
                for material, rate in factory.inputs.items():
                    self.IOMap[material] = self.IOMap.get(material, 0) - rate
                self.IOMap[M.POWER] = self.IOMap.get(M.POWER, 0) + factory.power
        if materials is not None:
            for material in materials:
                self.IOMap[material] = self.IOMap.get(material, 0) + 1

    def __repr__(self):
        return "{\n\tFactories: " + ", ".join([f'{factory.name}: {count}' for factory, count in self.factories.items()]) + ",\n\tInputs & Outputs: " + str(self.IOMap) + "\n}"

    def __add__(self, other):
        if isinstance(other, Factory):
            return FactoryGroup(factories = [other], factory_group = self)
        if isinstance(other, M.Material):
            return FactoryGroup(materials = [other], factory_group = self)
        if isinstance(other, FactoryGroup):
            result = FactoryGroup(factory_group = self)
            for factory_id, count in other.factories.items():
                result.factories[factory_id] = result.factories.get(factory_id, 0) + count
            for material, rate in other.IOMap.items():
                result.IOMap[material] = result.IOMap.get(material, 0) + rate
                if result.IOMap[material] == 0:
                    del result.IOMap[material]
            return result
        raise TypeError(f"unsupported operand type(s) for +: 'FactoryGroup' and '{type(other)}'")
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __sub__(self, other):
        return (-1 * self).__add__(other)
        
    def __rsub__(self, other):
        return self.__sub__(other)
    
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            result = FactoryGroup(factory_group = self)
            result.factories = {factory_id: count * other for factory_id, count in result.factories.items()}
            result.IOMap = {material: rate * other for material, rate in result.IOMap.items()}
            return result
        raise TypeError(f"unsupported operand type(s) for *: 'FactoryGroup' and '{type(other)}'")

    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __matmul__(self, other):
        return self + (self/other) * other # I'm realizing now that this is awful syntax. 

    def __truediv__(self, other):
        'Returns the number of "other" factory grroups required to supply this factory group'
        if isinstance(other, int) or isinstance(other, float):
            return self.__mul__(1/other)
        if isinstance(other, Factory):
            other = FactoryGroup(factories = [other])
        if isinstance(other, M.Material):
            other = FactoryGroup(materials = [other])
        if not isinstance(other, FactoryGroup):
            raise TypeError(f"unsupported operand type(s) for /: 'FactoryGroup' and '{type(other)}'")
        
        inputs = {material: rate for material, rate in self.IOMap.items() if rate < 0}
        outputs = {material: rate for material, rate in other.IOMap.items() if rate > 0}
        shared_keys = set(inputs.keys()) & set(outputs.keys())
        ratio = max(-inputs[material]/outputs[material] for material in shared_keys)
        return ratio

    def get_inputs(self):
        return {material: rate for material, rate in self.IOMap.items() if rate < 0}
    
    def get_outputs(self):
        return {material: rate for material, rate in self.IOMap.items() if rate > 0}


### 2. DRILLS ###
# I know these are resources gathering, but they function much more like factories than drills
@dataclass
class WaterExtractor(Factory):
    name: str = 'Water Extractor'
    id: int = 205
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=dict)
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.WATER: 6.6})
    power: int = -90
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class Cultivator(Factory):
    name: str = 'Cultivator'
    id: int = 206
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.WATER: 18})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SPORE_POD: .6})
    power: int = -80
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class OilExtractor(Factory):
    name: str = 'Oil Extractor'
    id: int = 207
    size: int = 3
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SAND:1, M.WATER: 9})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.OIL: 15})
    power: int = -180
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__


### 7. FACTORIES ###
@dataclass
class GraphitePress(Factory):
    name: str = 'Graphite Press'
    id: int = 701
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COAL: 1.33})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.GRAPHITE: .66})
    power: int = 0
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class MultiPress(Factory):
    name: str = 'Multi Press'
    id: int = 702
    size: int = 3
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COAL: 6, M.WATER: 6})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.GRAPHITE: 4})
    power: int = -108
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class SiliconSmelter(Factory):
    name: str = 'Silicon Smelter'
    id: int = 703
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COAL: 1.5, M.SAND: 3})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SILICON: 1.5})
    power: int = -30
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class SiliconCrucible(Factory):
    name: str = 'Silicon Crucible'
    id: int = 704
    size: int = 3
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COAL: 2.66, M.SAND: 4, M.PYRATITE: 0.66})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SILICON: 5.33})
    power: int = -240
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class Kiln(Factory):
    name: str = 'Kiln'
    id: int = 705
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.LEAD: 2, M.SAND: 2})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.METAGLASS: 2})
    power: int = -36
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class PlastaniumCompressor(Factory):
    name: str = 'Plastanium Compressor'
    id: int = 706
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.TITANIUM: 2, M.OIL: 15})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.PLASTANIUM: 1})
    power: int = -180
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class PhaseWeaver(Factory):
    name: str = 'Phase Weaver'
    id: int = 707
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.THORIUM: 2, M.SAND: 5})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.PHASE_FABRIC: 0.5})
    power: int = -300
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class SurgeSmelter(Factory):
    name: str = 'Surge Smelter'
    id: int = 708
    size: int = 3
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COPPER: 2.4, M.LEAD: 3.2, M.SILICON: 2.4, M.TITANIUM: 1.6})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SURGE_ALLOY: 0.8})
    power: int = -240
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class CryofluidMixer(Factory):
    name: str = 'Cryofluid Mixer'
    id: int = 709
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.WATER: 12, M.TITANIUM: .5})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.CRYOFLUID: 12})
    power: int = -60
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class PyratiteMixer(Factory):
    name: str = 'Pyratite Mixer'
    id: int = 710
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COAL: .75, M.LEAD: 1.5, M.SAND: 1.5})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.PYRATITE: .75})
    power: int = -12
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class BlastMixer(Factory):
    name: str = 'Blast Mixer'
    id: int = 711
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.PYRATITE: .75, M.SPORE_POD: .75})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.BLAST_COMPOUND: .75})
    power: int = -24
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class Melter(Factory):
    name: str = 'Melter'
    id: int = 712
    size: int = 1
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SCRAP: 6 })
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SLAG: 12})
    power: int = -60
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

# TODO: implement these
# @dataclass
# class Separator(Factory):
#     name: str = 'Separator'
#     id: int = 713
#     size: int = 2
#     inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SLAG: 4})
#     # Output ratio is 5:3:2:2
#     # .58 per second overall
#     # output = .58/12 * ratio, or .0483 * ratio
#     outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COPPER: 5*.0483, M.LEAD: 3*.0483, M.TITANIUM: 2*.0483, M.GRAPHITE: 2*.0483})
#     power: int = 0
# )

# @dataclass
# class Dissassembler(Factory):
#     name: str = 'Dissassembler'
#     id: int = 714
#     size: int = 3
#     inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SCRAP: 4, M.SLAG: 7.2})
#     # Output ratio is 2:4:2:1
#     # .25 per second overall
#     # output = .25/9 * ratio, or .0278 * ratio
#     outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.GRAPHITE: 2*.0278, M.SAND: 4*.0278, M.TITANIUM: 2*.0278, M.THORIUM: 1*.0278})
#     power: int = 0
# )

@dataclass
class SporePress(Factory):
    name: str = 'Spore Press'
    id: int = 715
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SPORE_POD: 3})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.OIL: 18})
    power: int = -42
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class Pulverizer(Factory):
    name: str = 'Pulverizer'
    id: int = 716
    size: int = 1
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SCRAP: 1.5})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SLAG: 1.5})
    power: int = -30
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class CoalCentrifuge(Factory):
    name: str = 'Coal Centrifuge'
    id: int = 717
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.OIL: 6})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COAL: 2})
    power: int = -42
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

# TODO: I haven't figured out optional inputs yet
# @dataclass
# class Incinerator(Factory):
#     name: str = 'Incinerator'
#     id: int = 718
#    size: int = 1
#     inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SLAG: 1})
#     outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
#     power: int = 0
# )

### 5. GENERATORS ###

@dataclass
class CombustionGenerator(Factory):
    name: str = 'Combustion Generator'
    id: int = 507
    size: int = 1
    inputs: Dict[M.Material, float] = {M.COAL: .5},  #TODO: I haven't figured out optional inputs yet
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 60
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class ThermalGenerator(Factory):
    name: str = 'Thermal Generator'
    id: int = 508
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.WATER: 1})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 60
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class SteamGenerator(Factory):
    name: str = 'Steam Generator'
    id: int = 509
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory={M.COAL: 1/1.5, M.WATER: 6}) # TODO: I haven't figured out optional inputs yet
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 330
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class DifferentailGenerator(Factory):
    name: str = 'Differentail Generator'
    id: int = 510
    size: int = 3
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.PYRATITE: 1/3.66, M.CRYOFLUID: 6})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 1080
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class RTGGenerator(Factory):
    name: str = 'RTG Generator'
    id: int = 511
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.THORIUM: 1/14})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 270
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class SolarPanel(Factory):
    name: str = 'Solar Panel'
    id: int = 512
    size: int = 1
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 6
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class LargeSolarPanel(Factory):
    name: str = 'Large Solar Panel'
    id: int = 513
    size: int = 3
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 78
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class ThoriumReactor(Factory):
    name: str = 'Thorium Reactor'
    id: int = 514
    size: int = 3
    inputs: Dict[M.Material, float] = {M.THORIUM: 1/6, M.CRYOFLUID: 2.5}, # Should be 2.4, but did this for safety!
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 900
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class ImpactReactor(Factory):
    name: str = 'Impact Reactor'
    id: int = 515
    size: int = 4
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.BLAST_COMPOUND: 1/2.33, M.CRYOFLUID: 15})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 7800
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

FACTORIES = {
    factory.id: factory for factory in [
    WaterExtractor, Cultivator, OilExtractor,
    GraphitePress, MultiPress, SiliconSmelter, SiliconCrucible, Kiln, PlastaniumCompressor, PhaseWeaver, SurgeSmelter, CryofluidMixer, PyratiteMixer, BlastMixer, Melter, SporePress, Pulverizer, CoalCentrifuge,
    CombustionGenerator, ThermalGenerator, SteamGenerator, DifferentailGenerator, RTGGenerator, SolarPanel, LargeSolarPanel, ThoriumReactor, ImpactReactor,
    ]
}