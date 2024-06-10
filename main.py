from typing import Dict, Optional

import MindustryObject as MO
from Materials import *
from Factories import *
from Collectors import *

coal_supply = {
    COAL: CoalCentrifuge(),
    OIL: OilExtractor(),
    WATER: WaterExtractor(),
}

all_scrap = {
    COPPER: Separator(),
    LEAD: Separator(),
    GRAPHITE: Separator(),
    THORIUM: Dissassembler(),
    SAND: Pulverizer(),
}

homemade = coal_supply | all_scrap

if __name__ == '__main__':
    
    print(FactoryGroup(materials={SURGE_ALLOY: -30}).get_upstream(rounded=True))
    print()
    print(FactoryGroup(materials={BLAST_COMPOUND: -20}).get_upstream(rounded=True))
