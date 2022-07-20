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

    assert costs.co2_footprint == '47.17'
    assert costs.costs == '93.65'
    assert costs.delivery_time == '80.0'


def test_compute_blended_costs_correctly_computes_all_cost_properties_when_not_all_are_filled():
    first_material_as_dict = {
        'costs': Costs(co2_footprint=22.2, costs=77, delivery_time=80)
    }
    second_material_as_dict = {
        'costs': Costs(co2_footprint=55.5, costs='', delivery_time=11)
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict]
    costs = BlendingPropertiesCalculator.compute_blended_costs([0.25, 0.75], base_materials_as_dict)

    assert costs.co2_footprint == '47.17'
    assert costs.costs is None
    assert costs.delivery_time == '80.0'


def test_compute_mean_finds_weighted_average_if_all_values_are_filled():
    first_material_as_dict = {
        'composition': Composition(fe3_o2='1.2')
    }
    second_material_as_dict = {
        'composition': Composition(fe3_o2='3.6')
    }
    third_material_as_dict = {
        'composition': Composition(fe3_o2='30')
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict, third_material_as_dict]
    mean = BlendingPropertiesCalculator.compute_mean([0.4, 0.4, 0.2], base_materials_as_dict,
                                                     'composition', 'fe3_o2')

    assert mean == '7.92'


def test_compute_mean_returns_none_when_not_all_values_are_filled():
    first_material_as_dict = {
        'composition': Composition(fe3_o2='1.2')
    }
    second_material_as_dict = {
        'composition': Composition(fe3_o2=None)
    }
    third_material_as_dict = {
        'composition': Composition(fe3_o2='30')
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict, third_material_as_dict]
    mean = BlendingPropertiesCalculator.compute_mean([0.4, 0.4, 0.2], base_materials_as_dict,
                                                     'composition', 'fe3_o2')

    assert mean is None


def test_compute_mean_returns_none_when_specified_property_does_not_exist():
    first_material_as_dict = {
        'composition': Composition(fe3_o2='1.2')
    }
    second_material_as_dict = {
        'composition': Composition(fe3_o2='1')
    }
    base_materials_as_dict = [first_material_as_dict, second_material_as_dict]

    mean = BlendingPropertiesCalculator.compute_mean([0.4, 0.4, 0.2], base_materials_as_dict, 'composition',
                                                     'not defined')
    assert mean is None
