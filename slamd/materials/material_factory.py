from werkzeug.exceptions import BadRequest, NotFound

from slamd.materials.forms.admixture_form import AdmixtureForm
from slamd.materials.forms.aggregates_form import AggregatesForm
from slamd.materials.forms.liquid_form import LiquidForm
from slamd.materials.forms.powder_form import PowderForm
from slamd.materials.forms.process_form import ProcessForm
from slamd.materials.material_type import MaterialType
from slamd.materials.strategies.aggregates_strategy import AggregatesStrategy
from slamd.materials.strategies.liquid_strategy import LiquidStrategy
from slamd.materials.strategies.powder_strategy import PowderStrategy
from slamd.materials.strategies.process_strategy import ProcessStrategy


class MaterialFactory:

    @classmethod
    def create_material_form(cls, type=None, submitted_material=None):
        if submitted_material is not None:
            type = submitted_material['material_type'].lower()

        if type == MaterialType.POWDER.value:
            cls = PowderForm
        elif type == MaterialType.LIQUID.value:
            cls = LiquidForm
        elif type == MaterialType.AGGREGATES.value:
            cls = AggregatesForm
        elif type == MaterialType.PROCESS.value:
            cls = ProcessForm
        elif type == MaterialType.ADMIXTURE.value:
            cls = AdmixtureForm
        else:
            raise NotFound

        if submitted_material is None:
            # Create an empty form
            return cls()
        else:
            # Populate a form with user data
            return cls(submitted_material)

    # TODO: add remaining strategies
    @classmethod
    def create_strategy(cls, type):
        if type == MaterialType.POWDER.value:
            return PowderStrategy()
        if type == MaterialType.LIQUID.value:
            return LiquidStrategy()
        if type == MaterialType.AGGREGATES.value:
            return AggregatesStrategy()
        if type == MaterialType.PROCESS.value:
            return ProcessStrategy()
        else:
            raise BadRequest
