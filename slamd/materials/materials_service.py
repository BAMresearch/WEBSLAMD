from werkzeug.exceptions import BadRequest

from slamd.materials.forms.admixture_form import AdmixtureForm
from slamd.materials.forms.aggregates_form import AggregatesForm
from slamd.materials.forms.base_materials_form import BaseMaterialsForm
from slamd.materials.forms.costs_form import CostsForm
from slamd.materials.forms.liquid_form import LiquidForm
from slamd.materials.forms.powder_form import PowderForm
from slamd.materials.forms.process_form import ProcessForm
from slamd.materials.material_type import MaterialType


class MaterialsService:

    def create_material_form(self, type):
        template_file = f'{type}_form.html'
        if type == MaterialType.POWDER.value:
            form = PowderForm()
        elif type == MaterialType.LIQUID.value:
            form = LiquidForm()
        elif type == MaterialType.AGGREGATES.value:
            form = AggregatesForm()
        elif type == MaterialType.PROCESS.value:
            form = ProcessForm()
        elif type == MaterialType.ADMIXTURE.value:
            form = AdmixtureForm()
        elif type == MaterialType.COSTS.value:
            form = CostsForm()
        else:
            raise BadRequest
        return template_file, form

    def create_additional_properties_form(self, num_fields):
        base_materials_form = BaseMaterialsForm()
        for i in range(num_fields):
            base_materials_form.additional_properties.append_entry(
                {'name': f'Prop {i+1}', 'value': ''})
        return base_materials_form
