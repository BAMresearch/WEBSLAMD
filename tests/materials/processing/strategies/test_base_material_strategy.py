from werkzeug.datastructures import ImmutableMultiDict

from slamd.materials.processing.material_dto import MaterialDto
from slamd.materials.processing.materials_persistence import MaterialsPersistence
from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.material import Material, Costs
from slamd.materials.processing.strategies.material_strategy import MaterialStrategy


class MockStrategy(MaterialStrategy):
    @classmethod
    def create_model(cls, submitted_material):
        return Material()

    @classmethod
    def gather_composition_information(cls, material):
        return


def test_base_material_strategy_include_returns_formatted_string():
    result = MockStrategy.include('test name', 'property')

    assert result == 'test name: property, '


def test_base_material_strategy_include_formats_numbers_with_precision_fifteen():
    result = MockStrategy.include('test name', 1.23456789123456789)

    # Number is rounded on the 15th decimal digit
    assert result == 'test name: 1.234567891234568, '


def test_base_material_strategy_include_returns_empty_string_if_empty_property():
    result = MockStrategy.include('test name', '')

    assert result == ''


def test_base_material_strategy_create_dto_without_properties():
    material = Material(
        name='test name',
        type='test type'
    )
    dto = MockStrategy.create_dto(material)

    assert isinstance(dto, MaterialDto)
    assert dto.uuid == str(material.uuid)
    assert dto.name == 'test name'
    assert dto.type == 'test type'
    assert dto.all_properties == ''


def test_base_material_strategy_convert_to_multidict_adds_all_properties():
    costs = Costs(
        co2_footprint=12.3,
        costs=45.6,
        delivery_time=789
    )
    material = Material(
        name='test material',
        type='Material',
        specific_gravity=1.40,
        costs=costs,
        additional_properties=[],
    )

    multidict = MockStrategy.convert_to_multidict(material)
    assert multidict['material_name'] == 'test material'
    assert multidict['material_type'] == 'Material'
    assert multidict['specific_gravity'] == 1.40
    assert multidict['co2_footprint'] == '12.3'
    assert multidict['costs'] == '45.6'
    assert multidict['delivery_time'] == '789'


def test_base_material_strategy_convert_to_multidict_adds_additional_properties():
    additional_properties = [AdditionalProperty('Prop 0', 'Value 0'),
                             AdditionalProperty('Prop 1', 'Value 1'),
                             AdditionalProperty('Prop 2', 'Value 2')]
    material = Material(
        name='test material',
        type='Material',
        costs=Costs(),
        additional_properties=additional_properties,
    )
    multidict = MockStrategy.convert_to_multidict(material)
    assert multidict['additional_properties-0-property_name'] == 'Prop 0'
    assert multidict['additional_properties-0-property_value'] == 'Value 0'
    assert multidict['additional_properties-1-property_name'] == 'Prop 1'
    assert multidict['additional_properties-1-property_value'] == 'Value 1'
    assert multidict['additional_properties-2-property_name'] == 'Prop 2'
    assert multidict['additional_properties-2-property_value'] == 'Value 2'


def test_base_material_strategy_extract_additional_properties_parses_additional_properties():
    submitted_material = ImmutableMultiDict([
        ('additional_properties-0-property_name', 'Prop 0'),
        ('additional_properties-0-property_value', 'Value 0'),
        ('additional_properties-1-property_name', 'Prop 1'),
        ('additional_properties-1-property_value', 'Value 1'),
        ('additional_properties-2-property_name', 'Prop 2'),
        ('additional_properties-2-property_value', 'Value 2')
    ])
    additional_properties = MockStrategy.extract_additional_properties(submitted_material)
    assert len(additional_properties) == 3
    assert additional_properties[0] == AdditionalProperty('Prop 0', 'Value 0')
    assert additional_properties[1] == AdditionalProperty('Prop 1', 'Value 1')
    assert additional_properties[2] == AdditionalProperty('Prop 2', 'Value 2')


def test_base_material_strategy_extract_cost_properties_parses_cost_properties():
    submitted_material = ImmutableMultiDict([
        ('co2_footprint', '12.3'),
        ('costs', '45.6'),
        ('delivery_time', '789'),
    ])
    costs = MockStrategy.extract_cost_properties(submitted_material)
    assert costs == Costs(co2_footprint=12.3, costs=45.6, delivery_time=789)


def test_base_material_strategy_edit_model_inyects_given_uuid():
    material = MockStrategy.edit_model('to_be_edited', ImmutableMultiDict())
    assert material.uuid == 'to_be_edited'


def test_base_material_strategy_save_model_saves_model(monkeypatch):
    mock_save_called_with = None

    def mock_save(type, model):
        nonlocal mock_save_called_with
        mock_save_called_with = (type, model)
        return None

    monkeypatch.setattr(MaterialsPersistence, 'save', mock_save)

    material = Material(name='test name', type='test type')
    MockStrategy.save_model(material)
    assert mock_save_called_with == ('test type', material)
