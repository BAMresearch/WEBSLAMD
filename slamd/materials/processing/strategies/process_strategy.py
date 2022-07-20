from slamd.common.slamd_utils import float_if_not_empty
from slamd.materials.processing.models.process import Process
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class ProcessStrategy(BaseMaterialStrategy):

    @classmethod
    def create_model(cls, submitted_material):
        return Process(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=cls.extract_cost_properties(submitted_material),
            duration=float_if_not_empty(submitted_material['duration']),
            temperature=float_if_not_empty(submitted_material['temperature']),
            relative_humidity=float_if_not_empty(submitted_material['relative_humidity']),
            additional_properties=cls.extract_additional_properties(submitted_material)
        )

    @classmethod
    def gather_composition_information(cls, process):
        return [cls.include('Duration', process.duration),
                cls.include('Temperature', process.temperature),
                cls.include('Relative Humidity', process.relative_humidity)]

    @classmethod
    def convert_to_multidict(cls, process):
        multidict = super().convert_to_multidict(process)
        multidict.add('duration', process.duration)
        multidict.add('temperature', process.temperature)
        multidict.add('relative_humidity', process.relative_humidity)
        return multidict
