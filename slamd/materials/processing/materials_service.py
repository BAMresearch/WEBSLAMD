from abc import ABC, abstractmethod
from dataclasses import dataclass
from slamd.materials.processing.material_factory import MaterialFactory
from slamd.materials.processing.material_type import MaterialType
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.material import Material


class MaterialsService(ABC):

    @classmethod
    def list_materials(cls, blended):
        all_material_types = MaterialType.get_all_types()

        all_material_dtos = []
        for material_type in all_material_types:
            strategy = MaterialFactory.create_strategy(material_type)
            all_materials = MaterialsPersistence.query_by_type(material_type)

            dtos_given_type = [strategy.create_dto(material)
                               for material in all_materials if material.is_blended == blended]
            all_material_dtos.extend(dtos_given_type)

        sorted_by_name = sorted(all_material_dtos, key=lambda material: material.name)
        sorted_by_type = sorted(sorted_by_name, key=lambda material: material.type)
        return cls.create_materials_response(sorted_by_type)

    @classmethod
    @abstractmethod
    def create_materials_response(cls, materials):
        pass


@dataclass
class MaterialsResponse:
    all_materials: list[Material]
    ctx: str
