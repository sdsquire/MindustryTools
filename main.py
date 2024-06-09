from typing import Dict, Optional

import MindustryObject as MO
from Materials import *
from Factories import *
from Collectors import *

get_power = lambda factory: factory @ ImpactReactor() @ CryofluidMixer() @ BlastMixer() @ PyratiteMixer() @ Cultivator() @ ImpactReactor()

def get_requirements(group: FactoryGroup, sources: Dict[M.Material, Factory | Collector]) -> FactoryGroup:
    while True:
        try:
            target_material = {material: rate for material, rate in group.IOMap.items() if rate < 0}.popitem()[0]
        except KeyError:
            break
        # Prefer specified source. Otherwise, prefer the most advanced source for natural materials or the factory that produces the material.
        if target_material in sources:
            source = sources[target_material]
        elif target_material is POWER:
            source = FACTORIES.items()[-1][1]
        elif not target_material.is_natural:
            for factory in FACTORIES.values():
                if target_material in factory.outputs:
                    source = factory
        elif target_material.is_liquid:
            source = list(PUMPS.items())[-1][1]
        else:
            source = list(DRILLS.items())[-1][1] # any other natural materials

        group @= source


if __name__ == '__main__':
    print(FactoryGroup(materials={PYRATITE:-40}) @ PyratiteMixer())
    