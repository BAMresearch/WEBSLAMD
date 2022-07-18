from slamd.materials.processing.models.process import Process
from slamd.materials.processing.strategies.base_material_strategy import MaterialStrategy


class ProcessStrategy(MaterialStrategy):

    def create_model(self, submitted_material):
        return Process(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=self.extract_cost_properties(submitted_material),
            duration=submitted_material['duration'],
            temperature=submitted_material['temperature'],
            relative_humidity=submitted_material['relative_humidity'],
            additional_properties=self.extract_additional_properties(submitted_material)
        )

    def gather_composition_information(self, process):
        return [self.include('Duration', process.duration),
                self.include('Temperature', process.temperature),
                self.include('Relative Humidity', process.relative_humidity)]

    def convert_to_multidict(self, process):
        multidict = super().convert_to_multidict(process)
        multidict.add('duration', process.duration)
        multidict.add('temperature', process.temperature)
        multidict.add('relative_humidity', process.relative_humidity)
        return multidict
