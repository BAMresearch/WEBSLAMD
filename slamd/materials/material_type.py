from enum import Enum


class MaterialType(Enum):
    POWDER = 'powder'
    LIQUID = 'liquid'
    AGGREGATES = 'aggregates'
    PROCESS = 'process'
    ADMIXTURE = 'admixture'
    CUSTOM = 'custom'

    @staticmethod
    def get_all_types():
        return [e.value for e in MaterialType]
