from dataclasses import dataclass, field
from typing import Dict, Optional, List

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
    IOMap: Dict[M.Material, float] = None

    def __post_init__(self):
        if self.IOMap is not None:
            return
        if self.inputs is None or self.outputs is None:
            raise TypeError(f"Factory.__init__() missing 1 required keyword-only argument: '{'inputs' if self.inputs is None else 'outputs'}'")
        self.IOMap = self.outputs
        for material, rate in self.inputs.items():
            self.IOMap[material] = self.IOMap.get(material, 0) - rate
        self.IOMap[M.POWER] = self.power # TODO: Should the user be able to put in the power as an input?

        for material in self.IOMap:
            material.sources.append(self)
    
    def __add__(self, other):
        'Combines the input and output of both factories.'
        if isinstance(other, Factory):
            extra_IO = other.IOMap.copy()
        elif isinstance(other, M.Material):
            extra_IO = {other: 1}
        elif isinstance(other, dict):
            if not all(isinstance(key, M.Material) for key in other):
                raise TypeError(f"unsupported operand type(s) for +: 'dict' can only be added to 'Factory' if all keys are of type 'Material'")
            extra_IO = other
        else:
            raise TypeError(f"unsupported operand type(s) for +: 'Factory' and '{type(other)}'")

        combined_IO = self.IOMap.copy()
        for material, rate in extra_IO.items():
            combined_IO[material] = round(combined_IO.get(material, 0) + rate, 2)
            if combined_IO[material] == 0:
                del combined_IO[material]

        return Factory( # TODO: figure out how to handle ids, names, etc. Maybe a combined class?
            id = 9999,
            name = self.name + ' + ' + other.name if isinstance(other, MindustryObject) else self.name + ' + ' + str(other),
            power = self.power + other.power,
            size = None,
            IOMap = combined_IO
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        'Removes the inputs and outputs of the other factory from this one.'
        return self + -1 * other

    def __rsub__(self, other):
        return self.__sub__(other)
  
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Factory(
                id = self.id,
                name = self.name,
                power = self.power * other,
                size = self.size,
                IOMap = {material: rate * other for material, rate in self.IOMap.items()}
            )
        raise TypeError(f"unsupported operand type(s) for *: 'Factory' and '{type(other)}'")
        
    def __rmul__(self, other):
        if isinstance(other, int):
            return self.__mul__(other)
        raise TypeError(f"unsupported operand type(s) for *: 'Factory' and '{type(other)}'")

    def __matmul__(self, other):
        'Combines two factories such that the output of one is fully covered by the input of the other.'
        if not isinstance(other, Factory):
            raise TypeError(f"unsupported operand type(s) for @: 'Factory' and '{type(other)}'")
        inputs = {material: -rate for material, rate in self.IOMap.items() if rate < 0}
        outputs = {material: rate for material, rate in other.IOMap.items() if rate > 0}
        combined_keys = set(inputs.keys()) & set(outputs.keys())
        ratios = [inputs[key] / outputs[key] for key in combined_keys]
        ratio = max(ratios)
        combined = self + other * ratio
        combined.IOMap = {material: rate for material, rate in combined.IOMap.items() if rate != 0}
        return combined
    
    def __div__(self, other):
        'Determines how many of the other factory are needed to keep up with this one. Returns a float.'
        if isinstance(other, int) or isinstance(other, float):
            return self * (1 / other)
        if isinstance(other, Factory):
            outputs = {material: rate for material, rate in other.IOMap.items() if rate > 0}
            inputs = {material: -rate for material, rate in self.IOMap.items() if rate < 0}
            combined_keys = set(inputs.keys()) & set(outputs.keys())
            ratios = [inputs[key] / outputs[key] for key in combined_keys]
            ratio = max(ratios)
            return ratio
        raise TypeError(f"unsupported operand type(s) for /: 'Factory' and '{type(other)}'")

class FactoryGroup():
    'This treats a group of factories as a single entity.'
    def __init__(self, factories: List[Factory] = None, *, materials: Optional[List[M.Material]] = None):
        self.factories = dict()
        self.IOMap = dict()
        if factories is not None:
            for factory in factories: # Combine inputs and outputs of all factories
                self.factories[factory.id] = self.factories.get(factory.id, 0) + 1 # TODO: Remove id and freeze dataclasses
                for material, rate in factory.outputs.items():
                    self.IOMap[material] = self.IOMap.get(material, 0) + rate
                for material, rate in factory.inputs.items():
                    self.IOMap[material] = self.IOMap.get(material, 0) - rate
                self.IOMap[M.POWER] = self.IOMap.get(M.POWER, 0) + factory.power
        if materials is not None:
            for material in materials:
                self.IOMap[material] = self.IOMap.get(material, 0) + 1

    def __add__(self, other):
        if isinstance(other, Factory):
            return self + FactoryGroup([other])
        if isinstance(other, M.Material):
            return

        


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

@dataclass
class Cultivator(Factory):
    name: str = 'Cultivator'
    id: int = 206
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.WATER: 18})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SPORE_POD: .6})
    power: int = -80

@dataclass
class OilExtractor(Factory):
    name: str = 'Oil Extractor'
    id: int = 207
    size: int = 3
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SAND:1, M.WATER: 9})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.OIL: 15})
    power: int = -180


### 7. FACTORIES ###
@dataclass
class GraphitePress(Factory):
    name: str = 'Graphite Press'
    id: int = 701
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COAL: 1.33})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.GRAPHITE: .66})
    power: int = 0

@dataclass
class MultiPress(Factory):
    name: str = 'Multi Press'
    id: int = 702
    size: int = 3
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COAL: 6, M.WATER: 6})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.GRAPHITE: 4})
    power: int = -108

@dataclass
class SiliconSmelter(Factory):
    name: str = 'Silicon Smelter'
    id: int = 703
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COAL: 1.5, M.SAND: 3})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SILICON: 1.5})
    power: int = -30

@dataclass
class SiliconCrucible(Factory):
    name: str = 'Silicon Crucible'
    id: int = 704
    size: int = 3
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COAL: 2.66, M.SAND: 4, M.PYRATITE: 0.66})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SILICON: 5.33})
    power: int = -240

@dataclass
class Kiln(Factory):
    name: str = 'Kiln'
    id: int = 705
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.LEAD: 2, M.SAND: 2})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.METAGLASS: 2})
    power: int = -36

@dataclass
class PlastaniumCompressor(Factory):
    name: str = 'Plastanium Compressor'
    id: int = 706
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.TITANIUM: 2, M.OIL: 15})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.PLASTANIUM: 1})
    power: int = -180

@dataclass
class PhaseWeaver(Factory):
    name: str = 'Phase Weaver'
    id: int = 707
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.THORIUM: 2, M.SAND: 5})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.PHASE_FABRIC: 0.5})
    power: int = -300

@dataclass
class SurgeSmelter(Factory):
    name: str = 'Surge Smelter'
    id: int = 708
    size: int = 3
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COPPER: 2.4, M.LEAD: 3.2, M.SILICON: 2.4, M.TITANIUM: 1.6})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SURGE_ALLOY: 0.8})
    power: int = -240

@dataclass
class CryofluidMixer(Factory):
    name: str = 'Cryofluid Mixer'
    id: int = 709
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.WATER: 12, M.TITANIUM: .5})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.CRYOFLUID: 12})
    power: int = -60

@dataclass
class PyratiteMixer(Factory):
    name: str = 'Pyratite Mixer'
    id: int = 710
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COAL: .75, M.LEAD: 1.5, M.SAND: 1.5})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.PYRATITE: .75})
    power: int = -12

@dataclass
class BlastMixer(Factory):
    name: str = 'Blast Mixer'
    id: int = 711
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.PYRATITE: .75, M.SPORE_POD: .75})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.BLAST_COMPOUND: .75})
    power: int = -24

@dataclass
class Melter(Factory):
    name: str = 'Melter'
    id: int = 712
    size: int = 1
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SCRAP: 6 })
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SLAG: 12})
    power: int = -60

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

@dataclass
class Pulverizer(Factory):
    name: str = 'Pulverizer'
    id: int = 716
    size: int = 1
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SCRAP: 1.5})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SLAG: 1.5})
    power: int = -30

@dataclass
class CoalCentrifuge(Factory):
    name: str = 'Coal Centrifuge'
    id: int = 717
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.OIL: 6})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COAL: 2})
    power: int = -42

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

@dataclass
class ThermalGenerator(Factory):
    name: str = 'Thermal Generator'
    id: int = 508
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.WATER: 1})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 60

@dataclass
class SteamGenerator(Factory):
    name: str = 'Steam Generator'
    id: int = 509
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory={M.COAL: 1/1.5, M.WATER: 6}) # TODO: I haven't figured out optional inputs yet
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 330

@dataclass
class DifferentailGenerator(Factory):
    name: str = 'Differentail Generator'
    id: int = 510
    size: int = 3
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.PYRATITE: 1/3.66, M.CRYOFLUID: 6})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 1080

@dataclass
class RTGGenerator(Factory):
    name: str = 'RTG Generator'
    id: int = 511
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.THORIUM: 1/14})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 270

@dataclass
class SolarPanel(Factory):
    name: str = 'Solar Panel'
    id: int = 512
    size: int = 1
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 6

@dataclass
class LargeSolarPanel(Factory):
    name: str = 'Large Solar Panel'
    id: int = 513
    size: int = 3
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 78

@dataclass
class ThoriumReactor(Factory):
    name: str = 'Thorium Reactor'
    id: int = 514
    size: int = 3
    inputs: Dict[M.Material, float] = {M.THORIUM: 1/6, M.CRYOFLUID: 2.5}, # Should be 2.4, but did this for safety!
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 900

@dataclass
class ImpactReactor(Factory):
    name: str = 'Impact Reactor'
    id: int = 515
    size: int = 4
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.BLAST_COMPOUND: 1/2.33, M.CRYOFLUID: 15})
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {})
    power: int = 7800

FACTORIES = [
    WaterExtractor, Cultivator, OilExtractor,
    GraphitePress, MultiPress, SiliconSmelter, SiliconCrucible, Kiln, PlastaniumCompressor, PhaseWeaver, SurgeSmelter, CryofluidMixer, PyratiteMixer, BlastMixer, Melter, SporePress, Pulverizer, CoalCentrifuge,
    CombustionGenerator, ThermalGenerator, SteamGenerator, DifferentailGenerator, RTGGenerator, SolarPanel, LargeSolarPanel, ThoriumReactor, ImpactReactor,
]