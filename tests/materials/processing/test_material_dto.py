from slamd.materials.processing.material_dto import MaterialDto


def test_material_dto_constructor_sets_default_values():
    material_dto = MaterialDto()

    assert material_dto.uuid == ''
    assert material_dto.name == ''
    assert material_dto.type == ''
    assert material_dto.all_properties == ''


def test_material_dto_constructor_sets_properties():
    material_dto = MaterialDto(
        uuid='a8098c1a-f86e-11da-bd1a-00112444be1e',
        name='test material DTO',
        material_type='test type',
        all_properties='prop0: test property, prop1: 12345'
    )

    assert material_dto.uuid == 'a8098c1a-f86e-11da-bd1a-00112444be1e'
    assert material_dto.name == 'test material DTO'
    assert material_dto.type == 'test type'
    assert material_dto.all_properties == 'prop0: test property, prop1: 12345'
