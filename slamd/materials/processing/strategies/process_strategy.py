from slamd.common.slamd_utils import float_if_not_empty, str_if_not_none
from slamd.materials.processing.models.process import Process
from slamd.materials.processing.strategies.material_strategy import MaterialStrategy


class ProcessStrategy(MaterialStrategy):

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
        return [cls.include('Duration (days)', process.duration),
                cls.include('Temperature (°C)', process.temperature),
                cls.include('Relative Humidity (%)', process.relative_humidity)]

    @classmethod
    def convert_to_multidict(cls, process):
        multidict = super().convert_to_multidict(process)
        multidict.add('duration', str_if_not_none(process.duration))
        multidict.add('temperature', str_if_not_none(process.temperature))
        multidict.add('relative_humidity', str_if_not_none(process.relative_humidity))
        return multidict

    @classmethod
    def for_formulation(cls, process):
        multidict = super().for_formulation(process)
        multidict.add('duration', float_if_not_empty(process.duration))
        multidict.add('temperature', float_if_not_empty(process.temperature))
        multidict.add('relative humidity', float_if_not_empty(process.relative_humidity))
        return multidict
