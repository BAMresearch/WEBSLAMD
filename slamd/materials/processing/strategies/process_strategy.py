from werkzeug.datastructures import MultiDict

from slamd.common.slamd_utils import float_if_not_empty, str_if_not_none
from slamd.materials.processing.models.process import Process
from slamd.materials.processing.strategies.material_strategy import MaterialStrategy


class ProcessStrategy(MaterialStrategy):

    @classmethod
    def create_material_from_dict(cls, dictionary):
        # Required for backwards compatibility with saved sessions from before 2025-02
        if "specific_gravity" not in dictionary:
            dictionary["specific_gravity"] = None
        if dictionary["costs"] is not None and "recyclingrate" not in dictionary["costs"]:
            dictionary["costs"]["recyclingrate"] = None

        mat = Process()
        cls.fill_material_object_with_basic_info_from_dict(mat, dictionary)
        return mat

    @classmethod
    def create_model(cls, submitted_material):
        return Process(
            name=submitted_material.get('material_name', None),
            type=submitted_material.get('material_type', None),
            costs=cls.extract_cost_properties(submitted_material),
            duration=float_if_not_empty(submitted_material.get('duration', None)),
            temperature=float_if_not_empty(submitted_material.get('temperature', None)),
            relative_humidity=float_if_not_empty(submitted_material.get('relative_humidity', None)),
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
        multidict = MultiDict()

        cls._convert_additional_properties_for_formulation(multidict, process)
        multidict.add('duration', float_if_not_empty(process.duration))
        multidict.add('temperature', float_if_not_empty(process.temperature))
        multidict.add('relative humidity', float_if_not_empty(process.relative_humidity))
        return multidict
