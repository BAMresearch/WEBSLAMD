from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.powder import Powder, Composition, Structure
from slamd.materials.processing.models.material import Costs


def test_powder_constructor_sets_default_values():
    powder = Powder()

    assert powder.name == ''
    assert powder.type == ''
    assert powder.costs is None
    assert powder.additional_properties is None
    assert powder.composition is None
    assert powder.structure is None


def test_powder_constructor_sets_properties():
    costs = Costs()
    composition = Composition()
    structure = Structure()
    powder = Powder(
        name='test powder',
        type='Powder',
        costs=costs,
        additional_properties=[AdditionalProperty(
            name='test prop', value='test value')],
        composition=composition,
        structure=structure
    )

    assert powder.name == 'test powder'
    assert powder.type == 'Powder'
    assert powder.costs == costs
    assert len(powder.additional_properties) == 1
    assert powder.composition == composition
    assert powder.structure == structure


def test_powder_composition_constructor_sets_default_values():
    composition = Composition()

    assert composition.fe3_o2 is None
    assert composition.si_o2 is None
    assert composition.al2_o3 is None
    assert composition.ca_o is None
    assert composition.mg_o is None
    assert composition.na2_o is None
    assert composition.k2_o is None
    assert composition.s_o3 is None
    assert composition.ti_o2 is None
    assert composition.p2_o5 is None
    assert composition.sr_o is None
    assert composition.mn2_o3 is None
    assert composition.loi is None


def test_powder_composition_constructor_sets_properties():
    composition = Composition(
        fe3_o2=12.3,
        si_o2=23.4,
        al2_o3=34.5,
        ca_o=45.6,
        mg_o=56.7,
        na2_o=67.8,
        k2_o=78.9,
        s_o3=89.0,
        ti_o2=0.98,
        p2_o5=9.87,
        sr_o=8.76,
        mn2_o3=7.65,
        loi=11.65
    )

    assert composition.fe3_o2 == 12.3
    assert composition.si_o2 == 23.4
    assert composition.al2_o3 == 34.5
    assert composition.ca_o == 45.6
    assert composition.mg_o == 56.7
    assert composition.na2_o == 67.8
    assert composition.k2_o == 78.9
    assert composition.s_o3 == 89.0
    assert composition.ti_o2 == 0.98
    assert composition.p2_o5 == 9.87
    assert composition.sr_o == 8.76
    assert composition.mn2_o3 == 7.65
    assert composition.loi == 11.65


def test_powder_structure_constructor_sets_default_values():
    structure = Structure()

    assert structure.fine is None


def test_powder_structure_constructor_sets_properties():
    structure = Structure(
        fine=123.45
    )

    assert structure.fine == 123.45
