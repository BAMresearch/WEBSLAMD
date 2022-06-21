from slamd.materials.forms.aggregates_form import AggregatesForm
from slamd.materials.forms.powder_form import PowderForm
from slamd.materials.forms.liquid_form import LiquidForm


class MaterialsService:

    def create_material_form(self, type):
        template_file = f'{type}_form.html'
        if type == 'powder':
            form = PowderForm()
        elif type == 'liquid':
            form = LiquidForm()
        elif type == 'aggregates':
            form = AggregatesForm()
        else:
            raise ValueError(f'Provided material type {type} is not supported')
        return template_file, form

