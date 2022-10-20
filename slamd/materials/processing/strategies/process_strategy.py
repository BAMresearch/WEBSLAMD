from werkzeug.datastructures import MultiDict

from slamd.common.slamd_utils import float_if_not_empty, str_if_not_none
from slamd.materials.processing.models.process import Process
from slamd.materials.processing.strategies.material_strategy import MaterialStrategy


class ProcessStrategy(MaterialStrategy):

    @classmethod
    def create_material_from_dict(cls, dictionary):
        mat = Process()
        cls.fill_material_object_with_basic_info_from_dict(mat, dictionary)
        return mat

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
        co2_footprint, costs = cls._adjust_units_to_match_with_materials(process)

        multidict = MultiDict([
            (f'delivery_time ({process.type})', float_if_not_empty(process.costs.delivery_time)),
            (f'costs ({process.type})', costs),
            (f'co2_footprint ({process.type})', co2_footprint),
        ])

        cls._convert_additional_properties_for_formulation(multidict, process)
        multidict.add('duration', float_if_not_empty(process.duration))
        multidict.add('temperature', float_if_not_empty(process.temperature))
        multidict.add('relative humidity', float_if_not_empty(process.relative_humidity))
        return multidict

    @classmethod
    def _adjust_units_to_match_with_materials(cls, process):
        """
        Costs for processes are measured in Euro while for materials they are measured in Euro / kg. Since in FormulationConverter
        within _postprocess_dataframe all costs are summed up and divided by 1000 (for converting to proper units for formulations)
        the corresponding processes must be adjusted accordingly. The most simple way is to scale them here.
        """
        costs = float_if_not_empty(process.costs.costs)
        if costs:
            costs *= 1000
        co2_footprint = float_if_not_empty(process.costs.co2_footprint)
        if co2_footprint:
            co2_footprint *= 1000
        return co2_footprint, costs
