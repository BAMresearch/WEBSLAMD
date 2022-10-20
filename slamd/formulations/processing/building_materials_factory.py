from slamd.common.error_handling import ValueNotSupportedException
from slamd.formulations.processing.building_material import BuildingMaterial
from slamd.formulations.processing.strategies.binder_strategy import BinderStrategy
from slamd.formulations.processing.strategies.concrete_strategy import ConcreteStrategy


class BuildingMaterialsFactory:

    @classmethod
    def create_building_material_strategy(cls, building_material):
        if building_material == BuildingMaterial.CONCRETE.value:
            return ConcreteStrategy
        elif building_material == BuildingMaterial.BINDER.value:
            return BinderStrategy
        else:
            raise ValueNotSupportedException(f'Received invalid building_material: {building_material}')
