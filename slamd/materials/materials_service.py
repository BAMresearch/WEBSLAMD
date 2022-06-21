from werkzeug.exceptions import BadRequest

from slamd.materials.forms.aggregates_form import AggregatesForm
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
        else:
            raise BadRequest()
        return template_file, form

