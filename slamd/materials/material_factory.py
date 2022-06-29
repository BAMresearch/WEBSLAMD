from werkzeug.exceptions import BadRequest, NotFound

from slamd.materials.forms.admixture_form import AdmixtureForm
from slamd.materials.forms.aggregates_form import AggregatesForm
from slamd.materials.forms.liquid_form import LiquidForm
from slamd.materials.forms.powder_form import PowderForm
from slamd.materials.forms.process_form import ProcessForm
from slamd.materials.material_type import MaterialType
from slamd.materials.strategies.liquid_strategy import LiquidStrategy
from slamd.materials.strategies.powder_strategy import PowderStrategy


class MaterialFactory:

    @classmethod
    def create_material_form(cls, type=None, submitted_material=None):
        if submitted_material is not None:
            type = submitted_material['material_type'].lower()

        if type == MaterialType.POWDER.value:
            return PowderForm() if submitted_material is None else PowderForm(submitted_material)
        elif type == MaterialType.LIQUID.value:
            return LiquidForm() if submitted_material is None else LiquidForm(submitted_material)
        elif type == MaterialType.AGGREGATES.value:
            return AggregatesForm() if submitted_material is None else AggregatesForm(submitted_material)
        elif type == MaterialType.PROCESS.value:
            return ProcessForm() if submitted_material is None else ProcessForm(submitted_material)
        elif type == MaterialType.ADMIXTURE.value:
            return AdmixtureForm() if submitted_material is None else AdmixtureForm(submitted_material)
        else:
            raise NotFound

    # TODO: add remaining strategies
    @classmethod
    def create_strategy(cls, type):
        if type == MaterialType.POWDER.value:
            return PowderStrategy()
        if type == MaterialType.LIQUID.value:
            return LiquidStrategy()
        else:
            raise BadRequest