from slamd.materials.processing.models.process import Process
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class ProcessStrategy(BaseMaterialStrategy):

    def create_model(self, submitted_material, additional_properties):
        process = Process(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=self.extract_costs_properties(submitted_material),
            duration=submitted_material['duration'],
            temperature=submitted_material['temperature'],
            relative_humidity=submitted_material['relative_humidity'],
            additional_properties=additional_properties
        )

        self.save_material(process)

    def gather_composition_information(self, process):
        return [self.include('Duration', process.duration),
                self.include('Temperature', process.temperature),
                self.include('Relative Humidity', process.relative_humidity)]
