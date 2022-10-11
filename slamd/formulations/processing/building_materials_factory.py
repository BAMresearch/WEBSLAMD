from slamd.common.error_handling import ValueNotSupportedException
from slamd.formulations.processing.building_material import BuildingMaterial
from slamd.formulations.processing.cement_strategy import CementStrategy
from slamd.formulations.processing.concrete_strategy import ConcreteStrategy


class BuildingMaterialsFactory:

    @classmethod
    def create_building_material_strategy(cls, building_material):
        if building_material == BuildingMaterial.CONCRETE.value:
            return ConcreteStrategy
        elif building_material == BuildingMaterial.CEMENT.value:
            return CementStrategy
        else:
            raise ValueNotSupportedException('No such building type!')
