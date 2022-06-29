from enum import Enum


class MaterialType(Enum):
    POWDER = 'powder'
    LIQUID = 'liquid'
    AGGREGATES = 'aggregates'
    PROCESS = 'process'
    ADMIXTURE = 'admixture'

    @staticmethod
    def get_all_types():
        return [MaterialType.POWDER.value,
                MaterialType.AGGREGATES.value,
                MaterialType.LIQUID.value,
                MaterialType.PROCESS.value,
                MaterialType.ADMIXTURE.value]
