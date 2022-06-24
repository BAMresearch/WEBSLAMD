from werkzeug.exceptions import BadRequest

from slamd.materials.forms.admixture_form import AdmixtureForm
from slamd.materials.forms.aggregates_form import AggregatesForm
from slamd.materials.forms.liquid_form import LiquidForm
from slamd.materials.forms.powder_form import PowderForm
from slamd.materials.forms.process_form import ProcessForm
from slamd.materials.material_type import MaterialType
from slamd.materials.model.additional_property import AdditionalProperty


class MaterialsService:

    def create_material_form(self, type):
        template_file = f'{type}_form.html'
        form = self._create_material_form(type)
        return template_file, form

    def save_material(self, type, submitted_material):
        form = self._create_material_form(type, submitted_material)

        if form.validate():
            additional_properties = []
            submitted_names = self._extract_additional_property_by_label(submitted_material, 'name')
            submitted_values = self._extract_additional_property_by_label(submitted_material, 'value')

            for name, value in zip(submitted_names, submitted_values):
                additional_property = AdditionalProperty(name, value)
                additional_properties.append(additional_property)

        return False, form

    def _extract_additional_property_by_label(self, submitted_material, label):
        return [submitted_material[k] for k in sorted(submitted_material) if
                'additional-properties' in k and label in k]

    def _create_material_form(self, type, submitted_material=None):
        if type == MaterialType.POWDER.value:
            form = PowderForm() if submitted_material is None else PowderForm(submitted_material)
        elif type == MaterialType.LIQUID.value:
            form = LiquidForm() if submitted_material is None else LiquidForm(submitted_material)
        elif type == MaterialType.AGGREGATES.value:
            form = AggregatesForm() if submitted_material is None else AggregatesForm(submitted_material)
        elif type == MaterialType.PROCESS.value:
            form = ProcessForm() if submitted_material is None else ProcessForm(submitted_material)
        elif type == MaterialType.ADMIXTURE.value:
            form = AdmixtureForm() if submitted_material is None else AdmixtureForm(submitted_material)
        else:
            raise BadRequest
        return form
