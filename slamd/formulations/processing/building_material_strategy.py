from abc import ABC, abstractmethod


class BuildingMaterialStrategy(ABC):

    @classmethod
    @abstractmethod
    def create_min_max_form(cls, formulation_selection):
        pass

    @classmethod
    @abstractmethod
    def populate_weigths_form(cls, weights_request_data):
        pass

    @classmethod
    @abstractmethod
    def _create_min_max_form_entry(cls, entries, uuids, name, type):
        pass

    @classmethod
    def _populate_common_ingredient_selection(cls, form, all_materials):
        form.powder_selection.choices = cls._to_selection(all_materials.powders)
        form.liquid_selection.choices = cls._to_selection(all_materials.liquids)
        form.aggregates_selection.choices = cls._to_selection(all_materials.aggregates_list)
        form.admixture_selection.choices = cls._to_selection(all_materials.admixtures)
        form.custom_selection.choices = cls._to_selection(all_materials.customs)
        form.process_selection.choices = cls._to_selection(all_materials.processes)
        return form

    @classmethod
    def _to_selection(cls, list_of_models):
        by_name = sorted(list_of_models, key=lambda model: model.name)
        by_type = sorted(by_name, key=lambda model: model.type)
        return list(map(lambda material: (f'{material.type}|{str(material.uuid)}', f'{material.name}'), by_type))

    @classmethod
    def _invalid_material_combination(cls, *names):
        for name in names:
            if len(name) == 0:
                return True
        return False

    @classmethod
    def _create_non_editable_entries(cls, formulation_selection, min_max_form, type):
        selection_for_type = [item for item in formulation_selection if item['type'] == type]
        for item in selection_for_type:
            cls._create_min_max_form_entry(min_max_form.non_editable_entries, item['uuid'], item['name'], type)
