from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List
from math import ceil

from MindustryObject import Building, MindustryException
import Materials as M
import Collectors as C

@dataclass
class Factory(Building):
    '''
    A factory building in Mindustry. This includes all buildings that take inputs and produce outputs.
    Note that this includes some things that are not classified as factories in-game, such as power generators and water extractors.

    Factories can be used with mathematical operations, which always result in a FactoryGroup. As such, see the FactoryGroup class for documentation on each operation.

    Args:
        name (str): The name of the factory.
        id (int): The ID of the factory.
        size (int): The size of the factory.
        inputs (Dict[M.Material, float]): The inputs of the factory.
        outputs (Dict[M.Material, float]): The outputs of the factory.
        power (int): The power usage of the factory.
        modal_efficiency (bool): Whether the building has efficiency options. Defaults to False.
        efficiency (float): The efficiency of the factory. Defaults to 1.0. If modal_efficiency is False, this must be 1.0 or an error is raised.
    '''
    inputs: Dict[M.Material, float] = None
    outputs: Dict[M.Material, float] = None
    efficiency: float = 1.0
    modal_efficiency: bool = False

    def __post_init__(self):
        if not self.modal_efficiency and self.efficiency != 1.0:
            raise ValueError(f"{self.name} has no options for efficiency (must be 1.0)")
        self.inputs =  {material: self.efficiency * rate for material, rate in self.inputs.items()}
        self.outputs =  {material: self.efficiency * rate for material, rate in self.outputs.items()}
        # for material, rate in self.outputs.items():
        #     self.outputs[material] = self.efficiency * rate
        #     material.set_source(self)
        
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
    modal_efficiency: bool = True
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
    modal_efficiency: bool = True
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
    modal_efficiency: bool = True
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
    modal_efficiency: bool = True
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
@dataclass
class Separator(Factory):
    name: str = 'Separator'
    id: int = 713
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SLAG: 4})
    # Output ratio is 5:3:2:2
    # .58 per second overall
    # output = .58/12 * ratio, or .0483 * ratio
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COPPER: 5*.0483, M.LEAD: 3*.0483, M.TITANIUM: 2*.0483, M.GRAPHITE: 2*.0483})
    power: int = 0
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class Dissassembler(Factory):
    name: str = 'Dissassembler'
    id: int = 714
    size: int = 3
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SCRAP: 4, M.SLAG: 7.2})
    # Output ratio is 2:4:2:1
    # .25 per second overall
    # output = .25/9 * ratio, or .0278 * ratio
    outputs: Dict[M.Material, float] = field(default_factory=lambda: {M.GRAPHITE: 2*.0278, M.SAND: 4*.0278, M.TITANIUM: 2*.0278, M.THORIUM: 1*.0278})
    power: int = 0
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

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
#     size: int = 1
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
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.COAL: .5}) #TODO: I haven't figured out optional inputs yet
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
    modal_efficiency: bool = True
    __hash__ = Factory.__hash__
    __eq__ = Factory.__eq__

@dataclass
class SteamGenerator(Factory):
    name: str = 'Steam Generator'
    id: int = 509
    size: int = 2
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.SPORE_POD: 1/1.5, M.WATER: 6}) # TODO: I haven't figured out optional inputs yet
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
    inputs: Dict[M.Material, float] = field(default_factory=lambda: {M.THORIUM: 1/6, M.CRYOFLUID: 2.5}) # Should be 2.4, but did this for safety!
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

# Quick lists for easy access
FACTORIES = {
    factory.id: factory for factory in [
    WaterExtractor(), Cultivator(), OilExtractor(),
    GraphitePress(), MultiPress(), SiliconSmelter(), SiliconCrucible(), Kiln(), PlastaniumCompressor(), PhaseWeaver(), SurgeSmelter(), CryofluidMixer(), PyratiteMixer(), BlastMixer(), Melter(), SporePress(), Pulverizer(), CoalCentrifuge(),
    CombustionGenerator(), ThermalGenerator(), SteamGenerator(), DifferentailGenerator(), RTGGenerator(), SolarPanel(), LargeSolarPanel(), ThoriumReactor(), ImpactReactor(),
    ]
}

GENERATORS = {
    factory.id: factory for factory in [
    CombustionGenerator(), ThermalGenerator(), SteamGenerator(), DifferentailGenerator(), RTGGenerator(), SolarPanel(), LargeSolarPanel(), ThoriumReactor(), ImpactReactor(),
    ]
}

SOURCES = {M.POWER: list(GENERATORS.values())}
for factory in FACTORIES.values():
    for material in factory.outputs:
        SOURCES[material] = SOURCES.get(material, []) + [factory]

class FactoryGroup():
    '''
    A group of factories. This is used to represent the combination of multiple factories, and can be combined using various mathematical operations.

    ATTRIBUTES:
        factories (Dict[Factory, float]): A dictionary of factories and their counts. Decimal values represent partial factory inputs / outputs. They are useful in calculation, but are not always reliable (ex. Impact reactors do not function with insufficient input).
        IOMap (Dict[M.Material, float]): A dictionary of the input/output materials and their rate in materials / second. Positive values are outputs, negative values are inputs.

    INITIALIZATION:
        The Factory group can be initialized with any of the following parameters. If multiple arguments are provided, all are combined; none are overridden.

        factories: These can be provided as a dictionary of factories and their counts, or as a list. If a list is provided, the counts are assumed to be 1.
        materials: These can be provided as a dictionary of materials and their counts, or as a list. If a list is provided, the counts are assumed to be 1.
        factory_group: If provided, all elements of the factory group are included in the new group.

    FUNCTIONS:

    OPERATORS:
        ADDITION (+): FactoryGroup, Factory, Material
            Combines two factory groups by adding all elements together.
            Can also be used to add a factory or material to a factory group. This is done by converting them to factory groups.
            
        SUBTRACTION (-): FactoryGroup, Factory, Material
            Subtracts two factory groups by subtracting all elements of the second group from the first group.
            Can also be used to subtract a factory or material from a factory group. This is done by converting them to factory groups.

        MULTIPLICATION (*): int, float
            Scales the factory group by a number. This is equivalent to multiplying all rates and all factories by that number.

        MATRIX MULTIPLICATION (@): Factory, FactoryGroup
            Combines two factories / factory groups. The second entity is scaled such that its output material rate matches the first entity's input rate for the corresponding material. If there are no shared materials, the entities are added together.
        
        DIVISION (/):
            If "other" is a FactoryGroup, returns the number of "other" factory groups required to supply this factory group. Dividing factories with no shared inputs/outputs will result in an error. If "other" is a number, scales the factory group by that amount (equivalent to multiplying by 1/other).
    '''
    def __init__(self, factories: Dict[Factory, float] | List[Factory]= None, *,  materials: Optional[Dict[M.Material, float]] | List[M.Material] = None, factory_group: Optional['FactoryGroup'] = None):
        self.factories = factory_group.factories.copy() if factory_group is not None else dict()
        self.IOMap = factory_group.IOMap.copy() if factory_group is not None else dict()

        if isinstance(factories, list):
            factories = {factory: 1 for factory in factories}
        if isinstance(materials, list):
            materials = {material: 1 for material in materials}

        if factories is not None:
            for factory, count in factories.items(): # Combine inputs and outputs of all factories
                self.factories[factory] = self.factories.get(factory, 0) + count
                for material, rate in factory.outputs.items():
                    self.IOMap[material] = self.IOMap.get(material, 0) + count * rate
                for material, rate in factory.inputs.items():
                    self.IOMap[material] = self.IOMap.get(material, 0) - count * rate
                self.IOMap[M.POWER] = self.IOMap.get(M.POWER, 0) + count * factory.power
        if materials is not None:
            for material, rate in materials.items():
                self.IOMap[material] = self.IOMap.get(material, 0) + rate

    def __repr__(self):
        output = '{'
        if self.factories:
            output += '\n   FACTORIES: [' + ', '.join(f'{factory.name}: {round(count,2)}' for factory, count in self.factories.items()) + ']'
        # if self.resources:
            # output += '\n   RESOURCES: [' + ', '.join(f'{material.name} tiles: {round(count,2)}' for material, count in self.resources.items()) + ']'
        if self.IOMap:
            output += '\n   INPUT / OUTPUT: [' + ', '.join(f'{material.name}: {round(rate,2)}' for material, rate in self.IOMap.items()) + ']'
        return output + '\n}' if output != '{' else '{}'
        

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
                if result.IOMap[material] < 0.0001 and result.IOMap[material] > -0.0001: # If is zero
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
        '''
        Combines two factories / factory groups.
        The second entity is scaled such that its output material rate matches the first entity's input rate for the corresponding material.
        If there are multiple shared materials, the second entity is scaled by the largest ratio (to ensure all materials are supplied).

        If there are no shared materials, the entities are added together.
        '''
        if isinstance(other, Factory):
            try:
                return self + (self/other) * other # This is some amazing syntax haha... Elegant, but might be too weird
            except MindustryException:
                return self + other
        raise TypeError(f"unsupported operand type(s) for @: 'FactoryGroup' and '{type(other)}'")

    def __rmatmul__(self, other):
        'Reverses the @ operator'
        if isinstance(other, Factory):
            return FactoryGroup(factories = [other]).__matmul__(self)
        
    def __truediv__(self, other):
        '''
        If "other" is a FactoryGroup, returns the number of "other" factory groups required to supply this factory group.
        Dividing factories with no shared inputs/outputs will result in an error.

        If "other" is a number, scales the factory group by that amount (equivalent to multiplying by 1/other).
        '''
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
        if not shared_keys:
            raise MindustryException(f"Cannot divide entity 1 by entity 2; entity 1 produces none of entity 2's inputs.")
        ratio = max(-inputs[material]/outputs[material] for material in shared_keys)
        return ratio
    
    def get_inputs(self):
        return {material: rate for material, rate in self.IOMap.items() if rate < 0}
    
    def get_outputs(self):
        return {material: rate for material, rate in self.IOMap.items() if rate > 0}

