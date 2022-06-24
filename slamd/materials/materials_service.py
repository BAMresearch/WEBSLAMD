from slamd.materials.material_factory import MaterialFactory
from slamd.materials.model.additional_property import AdditionalProperty


class MaterialsService:

    def create_material_form(self, type):
        template_file = f'{type}_form.html'
        form = MaterialFactory.create_material_form(type)
        return template_file, form

    # TODO: refactor -> path var not needed as it is passed as property of submitted_material
    def save_material(self, type, submitted_material):
        form = MaterialFactory.create_material_form(type, submitted_material)

        #if form.validate():
        additional_properties = []
        submitted_names = self._extract_additional_property_by_label(submitted_material, 'name')
        submitted_values = self._extract_additional_property_by_label(submitted_material, 'value')

        for name, value in zip(submitted_names, submitted_values):
            additional_property = AdditionalProperty(name, value)
            additional_properties.append(additional_property)

        self._create_base_material_by_type(type, submitted_material, additional_properties)
        #return False, form

    def _extract_additional_property_by_label(self, submitted_material, label):
        return [submitted_material[k] for k in sorted(submitted_material) if
                'additional-properties' in k and label in k]

    def _create_base_material_by_type(self, type, submitted_material, additional_properties):
        strategy = MaterialFactory.create_strategy(type)
        strategy.create_model(submitted_material, additional_properties)
