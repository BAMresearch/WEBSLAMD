from dataclasses import dataclass

from slamd.materials.processing.material_factory import MaterialFactory
from slamd.materials.processing.material_type import MaterialType
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.admixture import Admixture
from slamd.materials.processing.models.aggregates import Aggregates
from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.models.liquid import Liquid
from slamd.materials.processing.models.powder import Powder
from slamd.materials.processing.models.process import Process
from slamd.materials.processing.strategies.custom_strategy import CustomStrategy
from slamd.materials.processing.strategies.powder_strategy import PowderStrategy
from slamd.materials.processing.strategies.process_strategy import ProcessStrategy


@dataclass
class MaterialsForFormulations:
    powders: list[Powder]
    aggregates_list: list[Aggregates]
    liquids: list[Liquid]
    admixtures: list[Admixture]
    customs: list[Custom]
    processes: list[Process]


"""
Represents an API for accesses from another package, in particular formulations. All calls to materials from formulation
must be via using this facade.
"""


class MaterialsFacade:

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
    def materials_formulation_as_dict(cls, materials, processes):
        full_dict = {}
        names = []
        for material in materials:
            names.append(material.name)
            strategy = MaterialFactory.create_strategy(material.type.lower())
            full_dict = {**full_dict, **strategy.for_formulation(material)}
        for process in processes:
            full_dict = {**full_dict, **ProcessStrategy.for_formulation(process)}

        full_dict = {k: v for k, v in full_dict.items() if v is not None and v != ''}
        return full_dict, names
