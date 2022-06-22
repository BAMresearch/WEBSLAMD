from slamd.materials.materials_service import MaterialsService


def test_create_material_form_creates_powder():
    materials_service = MaterialsService()
    file, form = materials_service.create_material_form('powder')
    assert file == 'powder_form.html'
