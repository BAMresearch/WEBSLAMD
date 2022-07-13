from slamd.materials.processing.material_factory import MaterialFactory
from slamd.materials.processing.material_type import MaterialType
from slamd.materials.processing.materials_persistence import MaterialsPersistence


class MaterialsService:

    def list_materials(self, blended):
        all_material_types = MaterialType.get_all_types()

        all_material_dtos = []
        for material_type in all_material_types:
            all_materials = MaterialsPersistence.query_by_type(material_type)

            materials = list(filter(lambda material: material.is_blended == blended, all_materials))

            strategy = MaterialFactory.create_strategy(material_type)
            for material in materials:
                if not material.is_blended:
                    dto = strategy.create_dto(material)
                    all_material_dtos.append(dto)

        sorted_by_name = sorted(all_material_dtos, key=lambda material: material.name)
        sorted_by_type = sorted(sorted_by_name, key=lambda material: material.type)
        return sorted_by_type
