from dataclasses import dataclass, field

from slamd.common.slamd_utils import not_empty
from slamd.materials.processing.material_factory import MaterialFactory
from slamd.materials.processing.material_type import MaterialType
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.base_materials_service import BaseMaterialService
from slamd.materials.processing.models.admixture import Admixture
from slamd.materials.processing.models.aggregates import Aggregates
from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.models.liquid import Liquid
from slamd.materials.processing.models.powder import Powder
from slamd.materials.processing.models.process import Process


@dataclass
class MaterialsForFormulations:
    powders: list[Powder] = field(default_factory=list)
    aggregates_list: list[Aggregates] = field(default_factory=list)
    liquids: list[Liquid] = field(default_factory=list)
    admixtures: list[Admixture] = field(default_factory=list)
    customs: list[Custom] = field(default_factory=list)
    processes: list[Process] = field(default_factory=list)


class MaterialsFacade:
    """
    Represents an API for accesses from another package, in particular formulations. All calls to materials from formulation
    must be via using this facade.
    """

    POWDER = MaterialType.POWDER.value
    LIQUID = MaterialType.LIQUID.value
    AGGREGATES = MaterialType.AGGREGATES.value
    ADMIXTURE = MaterialType.ADMIXTURE.value
    CUSTOM = MaterialType.CUSTOM.value
    PROCESS = MaterialType.PROCESS.value

    @classmethod
    def find_all(cls):
        p = MaterialsPersistence
        return MaterialsForFormulations(powders=p.query_by_type(MaterialType.POWDER.value),
                                        aggregates_list=p.query_by_type(MaterialType.AGGREGATES.value),
                                        liquids=p.query_by_type(MaterialType.LIQUID.value),
                                        admixtures=p.query_by_type(MaterialType.ADMIXTURE.value),
                                        customs=p.query_by_type(MaterialType.CUSTOM.value),
                                        processes=p.query_by_type(MaterialType.PROCESS.value))

    @classmethod
    def get_material(cls, material_type, uuid):
        return MaterialsPersistence.query_by_type_and_uuid(material_type, uuid)

    @classmethod
    def get_process(cls, process_uuid):
        return cls.get_material('process', process_uuid)

    @classmethod
    def sort_for_concrete_formulation(cls, materials_for_formulation):
        sorted_materials = [materials_for_formulation.powders, materials_for_formulation.liquids]

        if len(materials_for_formulation.admixtures) > 0:
            sorted_materials.append(materials_for_formulation.admixtures)
        if len(materials_for_formulation.customs) > 0:
            sorted_materials.append(materials_for_formulation.customs)

        sorted_materials.append(materials_for_formulation.aggregates_list)

        return sorted_materials

    @classmethod
    def sort_for_binder_formulation(cls, materials_for_formulation):
        sorted_materials = [materials_for_formulation.liquids]

        if len(materials_for_formulation.aggregates_list) > 0:
            sorted_materials.append(materials_for_formulation.aggregates_list)
        if len(materials_for_formulation.admixtures) > 0:
            sorted_materials.append(materials_for_formulation.admixtures)
        if len(materials_for_formulation.customs) > 0:
            sorted_materials.append(materials_for_formulation.customs)

        sorted_materials.append(materials_for_formulation.powders)

        return sorted_materials

    @classmethod
    def materials_formulation_as_dict(cls, materials):
        full_dict = {}
        types = []
        names = []
        for material in list(materials):
            types.append(material.type)
            names.append(material.name)
            strategy = MaterialFactory.create_strategy(material.type.lower())
            full_dict = {**full_dict, **strategy.for_formulation(material)}

        full_dict = {k: v for k, v in full_dict.items() if not_empty(v)}
        return full_dict, types, names

    @classmethod
    def save_material(cls, material):
        material_uuid = BaseMaterialService.save_and_return_id(material)
        return material_uuid

    @classmethod
    def edit_material(cls, uuid, material):
        BaseMaterialService.do_edit(material['material_type'].lower(), str(uuid), material)

    @classmethod
    def get_material_from_session(cls, material, uuid):
        return MaterialsPersistence.query_by_type_and_uuid(material, str(uuid))
