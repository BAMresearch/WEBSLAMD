from slamd.materials.forms.aggregates_form import AggregatesForm
from slamd.materials.forms.powder_form import PowderForm
from slamd.materials.forms.liquid_form import LiquidForm


class MaterialsService:

    def create_material_form(self, type):
        material_type = type.lower()
        template_file = f'{type}_form.html'
        if material_type == 'powder':
            form = PowderForm()
        elif material_type == 'liquid':
            form = LiquidForm()
        elif material_type == 'aggregates':
            form = AggregatesForm()
        else:
            raise ValueError(f'Provided material type {material_type} is not supported')
        return template_file, form

