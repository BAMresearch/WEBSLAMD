from slamd.materials.processing.strategies.base_material_strategy import BaseMaterialStrategy


class MockStrategy(BaseMaterialStrategy):
    def create_model(self, submitted_material, additional_properties):
        return None


def test_base_material_strategy_include_returns_formatted_string():
    strategy = MockStrategy()
    result = strategy._include('test name', 'property')

    assert result == 'test name: property, '


def test_base_material_strategy_include_formats_numbers_with_precision_fifteen():
    strategy = MockStrategy()
    result = strategy._include('test name', 1.23456789123456789)

    # Number is rounded on the 15th decimal digit
    assert result == 'test name: 1.234567891234568, '


def test_base_material_strategy_include_returns_empty_string_if_empty_property():
    strategy = MockStrategy()
    result = strategy._include('test name', '')

    assert result == ''
