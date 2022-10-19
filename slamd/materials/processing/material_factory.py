from slamd.common.error_handling import MaterialNotFoundException
from slamd.materials.processing.forms.admixture_form import AdmixtureForm
from slamd.materials.processing.forms.aggregates_form import AggregatesForm
from slamd.materials.processing.forms.custom_form import CustomForm
from slamd.materials.processing.forms.liquid_form import LiquidForm
from slamd.materials.processing.forms.powder_form import PowderForm
from slamd.materials.processing.forms.process_form import ProcessForm
from slamd.materials.processing.material_type import MaterialType
from slamd.materials.processing.strategies.admixture_strategy import AdmixtureStrategy
from slamd.materials.processing.strategies.aggregates_strategy import AggregatesStrategy
from slamd.materials.processing.strategies.custom_strategy import CustomStrategy
from slamd.materials.processing.strategies.liquid_strategy import LiquidStrategy
from slamd.materials.processing.strategies.powder_strategy import PowderStrategy
from slamd.materials.processing.strategies.process_strategy import ProcessStrategy


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
        elif type == MaterialType.CUSTOM.value:
            cls = CustomForm
        else:
            raise MaterialNotFoundException(f'The requested type "{type}" is not supported!')

        if submitted_material is None:
            # Create an empty form, assigning the type in the correct format for the user
            return cls(material_type=type.capitalize())
        else:
            # Populate a form with user data
            return cls(submitted_material)

    @classmethod
    def create_strategy(cls, type):
        type = type.lower()
        if type == MaterialType.POWDER.value:
            return PowderStrategy
        if type == MaterialType.LIQUID.value:
            return LiquidStrategy
        if type == MaterialType.AGGREGATES.value:
            return AggregatesStrategy
        if type == MaterialType.PROCESS.value:
            return ProcessStrategy
        if type == MaterialType.ADMIXTURE.value:
            return AdmixtureStrategy
        if type == MaterialType.CUSTOM.value:
            return CustomStrategy
        else:
            raise MaterialNotFoundException(f'The requested type "{type}" is not supported!')
