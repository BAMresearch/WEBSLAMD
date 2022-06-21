from slamd.materials.forms.powder_form import PowderForm
from slamd.materials.forms.liquid_form import LiquidForm


class MaterialsService:
    def create_material_form(self, type):
        type = type.lower()
        template_file = f'{type}_form.html'
        if type == 'powder':
            form = PowderForm()
        elif type == 'liquid':
            form = LiquidForm()
        else:
            raise ValueError(f'Provided material type {type} is not supported')
        return template_file, form

