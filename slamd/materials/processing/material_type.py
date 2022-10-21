from enum import Enum


class MaterialType(Enum):
    POWDER = 'powder'
    LIQUID = 'liquid'
    AGGREGATES = 'aggregates'
    PROCESS = 'process'
    ADMIXTURE = 'admixture'
    CUSTOM = 'custom'

    @classmethod
    def get_all_types(cls):
        return [e.value for e in MaterialType]

    @classmethod
    def get_all_materials(cls):
        return [e.value for e in MaterialType if e.value != 'process']
