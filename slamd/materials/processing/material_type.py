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

    @classmethod
    def get_all_processes(cls):
        return [e.value for e in MaterialType if e.value == 'process']

    @classmethod
    def get_sorted(cls, sort_dict):
        all_types = cls.get_all_types()

        return sorted(all_types, key=lambda mat_type: [k for k, v in sort_dict.items() if v == mat_type][0])
