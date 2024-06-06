import Materials as M
import Factories as F

M.POWER.set_source(F.ImpactReactor())


def get_requirements(group: F.FactoryGroup) -> F.FactoryGroup:
    '''
    Get the requirements of a factory group.

    Args:
        group (FactoryGroup): The factory group to get the requirements of.

    Returns:
        FactoryGroup: The requirements of the factory group.
    '''
    while True:
        dependent_materials = {material: rate for material, rate in group.IOMap.items() if rate < 0 and not material.is_natural}
        if not dependent_materials:
            break
        target_material = dependent_materials.popitem()[0]
        group = group @ target_material.source


if __name__ == '__main__':
    print(get_requirements(60*F.PlastaniumCompressor()))
    # print(F.PlastaniumCompressor() @ F.OilExtractor())