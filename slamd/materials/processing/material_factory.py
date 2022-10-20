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
    def create_material_form(cls, material_type=None, submitted_material=None):
        if submitted_material is not None:
            material_type = submitted_material['material_type'].lower()

        if material_type == MaterialType.POWDER.value:
            form = PowderForm
        elif material_type == MaterialType.LIQUID.value:
            form = LiquidForm
        elif material_type == MaterialType.AGGREGATES.value:
            form = AggregatesForm
        elif material_type == MaterialType.PROCESS.value:
            form = ProcessForm
        elif material_type == MaterialType.ADMIXTURE.value:
            form = AdmixtureForm
        elif material_type == MaterialType.CUSTOM.value:
            form = CustomForm
        else:
            raise MaterialNotFoundException(f'The requested type "{material_type}" is not supported!')

        if submitted_material is None:
            # Create an empty form, assigning the type in the correct format for the user
            return form(material_type=material_type.capitalize())
        # Populate a form with user data
        return form(submitted_material)

    @classmethod
    def create_strategy(cls, material_type):
        material_type = material_type.lower()
        if material_type == MaterialType.POWDER.value:
            return PowderStrategy
        if material_type == MaterialType.LIQUID.value:
            return LiquidStrategy
        if material_type == MaterialType.AGGREGATES.value:
            return AggregatesStrategy
        if material_type == MaterialType.PROCESS.value:
            return ProcessStrategy
        if material_type == MaterialType.ADMIXTURE.value:
            return AdmixtureStrategy
        if material_type == MaterialType.CUSTOM.value:
            return CustomStrategy

        raise MaterialNotFoundException(f'The requested type "{material_type}" is not supported!')
