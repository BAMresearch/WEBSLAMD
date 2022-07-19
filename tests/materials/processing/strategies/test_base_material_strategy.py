from slamd.materials.processing.material_dto import MaterialDto
from slamd.materials.processing.models.material import Material
from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class MockStrategy(BaseMaterialStrategy):
    @classmethod
    def create_model(cls, submitted_material, additional_properties):
        return None

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
