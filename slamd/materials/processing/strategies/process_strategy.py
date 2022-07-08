from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.models.process import Process
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class ProcessStrategy(BaseMaterialStrategy):

    def create_model(self, submitted_material, additional_properties):
        costs = Costs(
            co2_footprint=submitted_material['co2_footprint'],
            delivery_time=submitted_material['delivery_time'],
            costs=submitted_material['costs']
        )

        process = Process(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=costs,
            duration=submitted_material['duration'],
            temperature=submitted_material['temperature'],
            relative_humidity=submitted_material['relative_humidity'],
            additional_properties=additional_properties
        )

        MaterialsPersistence.save('process', process)

    def _gather_composition_information(self, process):
        return [self._include('Duration', process.duration),
                self._include('Temperature', process.temperature),
                self._include('Relative Humidity', process.relative_humidity)]
