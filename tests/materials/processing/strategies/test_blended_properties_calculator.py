from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.models.powder import Composition
from slamd.materials.processing.strategies.blending_properties_calculator import BlendingPropertiesCalculator


def test_compute_blended_costs_correctly_computes_all_cost_properties_when_all_are_filled():
    first_material_as_dict = {
        'costs': Costs(co2_footprint=22.2, costs=77, delivery_time=80)
    }
    second_material_as_dict = {
        'costs': Costs(co2_footprint=55.5, costs=99.2, delivery_time=11)
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict]
    costs = BlendingPropertiesCalculator.compute_blended_costs([0.25, 0.75], base_materials_as_dict)

    assert costs.co2_footprint == 47.17
    assert costs.costs == 93.65
    assert costs.delivery_time == 80.0


def test_compute_blended_costs_correctly_computes_all_cost_properties_when_not_all_are_filled():
    first_material_as_dict = {
        'costs': Costs(co2_footprint=22.2, costs=77, delivery_time=80)
    }
    second_material_as_dict = {
        'costs': Costs(co2_footprint=55.5, delivery_time=11)
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict]
    costs = BlendingPropertiesCalculator.compute_blended_costs([0.25, 0.75], base_materials_as_dict)

    assert costs.co2_footprint == 47.17
    assert costs.costs is None
    assert costs.delivery_time == 80.0


def test_compute_mean_finds_weighted_average_if_all_values_are_filled():
    first_material_as_dict = {
        'composition': Composition(fe3_o2=1.2)
    }
    second_material_as_dict = {
        'composition': Composition(fe3_o2=3.6)
    }
    third_material_as_dict = {
        'composition': Composition(fe3_o2=30)
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict, third_material_as_dict]
    mean = BlendingPropertiesCalculator.compute_mean([0.4, 0.4, 0.2], base_materials_as_dict,
                                                     'composition', 'fe3_o2')

    assert mean == 7.92


def test_compute_mean_returns_none_when_not_all_values_are_filled():
    first_material_as_dict = {
        'composition': Composition(fe3_o2=1.2)
    }
    second_material_as_dict = {
        'composition': Composition()
    }
    third_material_as_dict = {
        'composition': Composition(fe3_o2=30)
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict, third_material_as_dict]
    mean = BlendingPropertiesCalculator.compute_mean([0.4, 0.4, 0.2], base_materials_as_dict,
                                                     'composition', 'fe3_o2')

    assert mean is None


def test_compute_mean_returns_none_when_specified_property_does_not_exist():
    first_material_as_dict = {
        'composition': Composition(fe3_o2=1.2)
    }
    second_material_as_dict = {
        'composition': Composition(fe3_o2=1)
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict]

    mean = BlendingPropertiesCalculator.compute_mean([0.4, 0.4, 0.2], base_materials_as_dict, 'composition',
                                                     'not defined')
    assert mean is None


def test_compute_additional_properties_creates_blended_properties_if_all_properties_specified_consistently():
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

    result = BlendingPropertiesCalculator.compute_additional_properties([0.4, 0.4, 0.2], base_materials_as_dict)

    assert len(result) is 4
    assert result[0].name == 'Prop 1'
    assert result[0].value == '10.44'
    assert result[1].name == 'X'
    assert result[1].value == '0.4'
    assert result[2].name == 'Y'
    assert result[2].value == '0.4'
    assert result[3].name == 'Z'
    assert result[3].value == '0.2'


def test_compute_additional_properties_creates_blended_properties_if_only_continuous_property_specified_consistently():
    first_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 1', '5'), AdditionalProperty('Prop 2', 'X')]
    }
    second_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 1', '10')]
    }
    third_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 1', '22.2'), AdditionalProperty('Prop 2', 'Z')]
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict, third_material_as_dict]

    result = BlendingPropertiesCalculator.compute_additional_properties([0.4, 0.4, 0.2], base_materials_as_dict)

    assert len(result) == 1
    assert result[0].name == 'Prop 1'
    assert result[0].value == '10.44'


# Note that for first_material_as_dict and second_material_as_dict the value of Prop 2 is X
def test_compute_additional_properties_creates_blended_properties_if_only_categorical_property_specified_consistently():
    first_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 1', '5'), AdditionalProperty('Prop 2', 'X')]
    }
    second_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 1', '10'), AdditionalProperty('Prop 2', 'X')]
    }
    third_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 2', 'Z')]
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict, third_material_as_dict]

    result = BlendingPropertiesCalculator.compute_additional_properties([0.4, 0.4, 0.2], base_materials_as_dict)

    assert len(result) == 2
    assert result[0].name == 'X'
    assert result[0].value == '0.8'
    assert result[1].name == 'Z'
    assert result[1].value == '0.2'


def test_compute_additional_properties_creates_blended_properties_if_categorical_has_wrong_value():
    first_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 1', '5'), AdditionalProperty('Prop 2', 'X')]
    }
    second_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 2', '17')]
    }
    third_material_as_dict = {
        'additional_properties': [AdditionalProperty('Prop 2', 'Z')]
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict, third_material_as_dict]

    result = BlendingPropertiesCalculator.compute_additional_properties([0.4, 0.4, 0.2], base_materials_as_dict)

    assert len(result) == 0
