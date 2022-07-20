from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.powder import Composition
from slamd.materials.processing.strategies.property_completeness_checker import PropertyCompletenessChecker


def test_is_complete_is_true_if_property_is_filled_for_all_base_materials():
    first_material_as_dict = {
        'composition': Composition(fe3_o2=17)
    }
    second_material_as_dict = {
        'composition': Composition(fe3_o2=20)
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict]
    complete = PropertyCompletenessChecker.is_complete(base_materials_as_dict, 'composition', 'fe3_o2')

    assert complete is True


def test_is_complete_is_false_if_property_is_not_filled_for_all_base_materials():
    first_material_as_dict = {
        'composition': Composition(fe3_o2=17)
    }
    second_material_as_dict = {
        'composition': Composition(si_o2=20)
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict]
    complete = PropertyCompletenessChecker.is_complete(base_materials_as_dict, 'composition', 'fe3_o2')

    assert complete is False


def test_is_complete_is_false_for_invalid_key():
    first_material_as_dict = {
        'composition': Composition(fe3_o2=17)
    }
    second_material_as_dict = {
        'composition': Composition(si_o2=20)
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict]
    complete = PropertyCompletenessChecker.is_complete(base_materials_as_dict, 'composition', 'invalid key')

    assert complete is False


def test_is_complete_with_values_returned_returns_all_values():
    first_material_as_dict = {
        'composition': Composition(fe3_o2=17)
    }
    second_material_as_dict = {
        'composition': Composition(fe3_o2=20)
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict]
    complete, values = PropertyCompletenessChecker.is_complete_with_values_returned(base_materials_as_dict, ('composition', 'fe3_o2'))

    assert complete is True
    assert len(values) == 2
    assert values[0] == 17
    assert values[1] == 20


def test_additional_properties_are_complete_succeed_when_all_additional_properties_in_all_base_materials():
    first_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 1', '5'), AdditionalProperty('Prop 2', 'X')]
    }
    second_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 1', '10'), AdditionalProperty('Prop 2', 'Y')]
    }
    third_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 1', '22.2'), AdditionalProperty('Prop 2', 'Z')]
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict, third_material_as_dict]
    complete = PropertyCompletenessChecker.additional_properties_are_complete(base_materials_as_dict)

    assert complete is True


def test_additional_properties_are_complete_fails_when_additional_property_misses_in_a_base_material_scenario1():
    first_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 2', 'X')]
    }
    second_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 1', '10'), AdditionalProperty('Prop 2', 'Y')]
    }
    third_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 1', '22.2'), AdditionalProperty('Prop 2', 'Z')]
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict, third_material_as_dict]
    complete = PropertyCompletenessChecker.additional_properties_are_complete(base_materials_as_dict)

    assert complete is False


def test_additional_properties_are_complete_fails_when_additional_property_misses_in_a_base_material_scenario2():
    first_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 1', '5'), AdditionalProperty('Prop 2', 'X')]
    }
    second_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 1', '10')]
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict]
    complete = PropertyCompletenessChecker.additional_properties_are_complete(base_materials_as_dict)

    assert complete is False


def test_additional_properties_are_complete_fails_when_inconsistent_values_for_a_property_are_set():
    first_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 1', '5'), AdditionalProperty('Prop 2', 'X')]
    }
    second_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 1', '10'), AdditionalProperty('Prop 2', '16')]
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict]
    complete = PropertyCompletenessChecker.additional_properties_are_complete(base_materials_as_dict)

    assert complete is False
