from slamd.discovery.processing.discovery_facade import DiscoveryFacade, TEMPORARY_FORMULATION
from slamd.formulations.processing.building_material import BuildingMaterial
from slamd.formulations.processing.building_material_strategy import BuildingMaterialStrategy
from slamd.formulations.processing.forms.cement_selection_form import CementSelectionForm
from slamd.materials.processing.materials_facade import MaterialsFacade


class CementStrategy(BuildingMaterialStrategy):

    @classmethod
    def populate_selection_form(cls):
        all_materials = MaterialsFacade.find_all()
        form = cls._populate_common_ingredient_selection(CementSelectionForm(), all_materials)
        return form, BuildingMaterial.CEMENT.value

    @classmethod
    def get_formulations(cls):
        dataframe = None
        temporary_dataset = DiscoveryFacade.query_dataset_by_name(TEMPORARY_FORMULATION)
        if temporary_dataset:
            dataframe = temporary_dataset.dataframe
        return dataframe
