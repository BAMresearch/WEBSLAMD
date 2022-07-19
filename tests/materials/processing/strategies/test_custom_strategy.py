from werkzeug.datastructures import ImmutableMultiDict
from slamd.materials.processing.models.custom import Custom
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.custom_strategy import CustomStrategy


def test_create_model_reads_all_properties_from_submitted_material():
    submitted_material = ImmutableMultiDict([('material_name', 'test custom'),
                                             ('material_type', 'Custom'),
                                             ('co2_footprint', '999.99'),
                                             ('costs', '888.88'),
                                             ('delivery_time', '77'),
                                             ('custom_name', 'test custom name'),
                                             ('custom_value', 'test custom value'),
                                             ('submit', 'Save material')])
    model = CustomStrategy.create_model(submitted_material)
    assert model.name == 'test custom'
    assert model.type == 'Custom'
    assert model.costs.co2_footprint == 999.99
    assert model.costs.costs == 888.88
    assert model.costs.delivery_time == 77
    assert model.custom_name == 'test custom name'
    assert model.custom_value == 'test custom value'


def test_gather_composition_properties_adds_all_properties():
    custom = Custom(
        name='test custom',
        type='Custom',
        costs=Costs(),
        additional_properties=[],
        custom_name='test custom name',
        custom_value='test custom value'
    )

    result = CustomStrategy.gather_composition_information(custom)
    assert result == ['Name: test custom name, ', 'Value: test custom value, ']


def test_convert_to_multidict_adds_all_properties():
    custom = Custom(
        name='test custom',
        type='Custom',
        costs=Costs(),
        additional_properties=[],
        custom_name='test custom name',
        custom_value='test custom value'
    )

    multidict = CustomStrategy.convert_to_multidict(custom)
    assert multidict['material_name'] == 'test custom'
    assert multidict['material_type'] == 'Custom'
    assert multidict['custom_name'] == 'test custom name'
    assert multidict['custom_value'] == 'test custom value'
