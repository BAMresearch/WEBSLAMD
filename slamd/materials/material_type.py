from enum import Enum


class MaterialType(Enum):
    POWDER = 'powder'
    LIQUID = 'liquid'
    AGGREGATES = 'aggregates'
    PROCESS = 'process'
    ADMIXTURE = 'admixture'
    COSTS = 'costs'
    CUSTOM = 'custom'

    # TODO: add remaining types
    @staticmethod
    def get_all_types():
        return [MaterialType.POWDER.value]
