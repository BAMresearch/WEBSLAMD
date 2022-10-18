from uuid import uuid1, UUID

from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.aggregates import Aggregates
from slamd.materials.processing.models.aggregates import Composition as AggComposition
from slamd.materials.processing.models.liquid import Liquid
from slamd.materials.processing.models.liquid import Composition as LiqComposition
from slamd.materials.processing.models.material import Material, Costs
from slamd.materials.processing.models.powder import Powder, Structure
from slamd.materials.processing.models.powder import Composition as PowComposition
from slamd.materials.processing.strategies.aggregates_strategy import AggregatesStrategy
from slamd.materials.processing.strategies.liquid_strategy import LiquidStrategy
from slamd.materials.processing.strategies.material_strategy import MaterialStrategy
from slamd.materials.processing.strategies.powder_strategy import PowderStrategy


def _create_generic_material():
    material_as_dict = {
        'name': 'MatName', 'type': 'generic',
        'uuid': str(uuid1()),
        'costs': {
            'co2_footprint': 1.2, 'costs': 2.3, 'delivery_time': 3.4
        },
        'additional_properties': [
            {'name': 'AddProp1', 'value': 5},
            {'name': 'AddProp2', 'value': 'val'},
        ],
        'is_blended': False, 'blending_ratios': 'Ratio', 'created_from': []
    }

    material = Material(**material_as_dict)
    material.uuid = UUID(material_as_dict['uuid'])
    material.costs = Costs(**material_as_dict['costs'])
    material.additional_properties = [AdditionalProperty(**prop) for prop in material_as_dict['additional_properties']]

    return material, material_as_dict


def _create_aggregates_material():
    aggregate_as_dict = {
        'name': 'AggName', 'type': 'aggregate',
        'composition': {
            'fine_aggregates': 1.2,
            'coarse_aggregates': 2.3,
            'gravity': 3.4,
            'bulk_density': 4.5,
            'fineness_modulus': 5.6,
            'water_absorption': 6.7
        }
    }

    aggregate = Aggregates(**aggregate_as_dict)
    aggregate.composition = AggComposition(**aggregate_as_dict['composition'])

    return aggregate, aggregate_as_dict


def _create_powder_material():
    powder_as_dict = {
        'name': 'PowName', 'type': 'powder',
        'composition': {
            'fe3_o2': 1.2,
            'si_o2': 2.3,
            'al2_o3': 3.4,
            'ca_o': 4.5,
            'mg_o': 5.6,
            'na2_o': 6.7,
            'k2_o': 7.8,
            's_o3': 8.9,
            'ti_o2': 9.1,
            'p2_o5': 1.2,
            'sr_o': 2.3,
            'mn2_o3': 3.4,
            'loi': 4.5
        },
        'structure': {
            'fine': 1.2,
            'gravity': 2.3
        }
    }

    powder = Powder(**powder_as_dict)
    powder.composition = PowComposition(**powder_as_dict['composition'])
    powder.structure = Structure(**powder_as_dict['structure'])

    return powder, powder_as_dict


def _create_liquid_material():
    liquid_as_dict = {
        'name': 'LiqName', 'type': 'liquid',
        'composition': {
            'na2_si_o3': 1.2,
            'na2_si_o3_mol': 2.3,
            'na_o_h': 3.4,
            'na_o_h_mol': 4.5,
            'na2_o': 5.6,
            'na2_o_mol': 6.7,
            'si_o2': 7.8,
            'si_o2_mol': 8.9,
            'h2_o': 9.1,
            'h2_o_mol': 1.2,
        }
    }

    liquid = Liquid(**liquid_as_dict)
    liquid.composition = LiqComposition(**liquid_as_dict['composition'])

    return liquid, liquid_as_dict


def test_generic_material_to_dict():
    material, material_as_dict = _create_generic_material()

    assert material_as_dict == MaterialStrategy.convert_material_to_dict(material)


def test_generic_material_from_dict():
    material, material_as_dict = _create_generic_material()
    mat_from_dict = MaterialStrategy.create_material_from_dict(material_as_dict)

    costs = material_as_dict.pop('costs')
    assert mat_from_dict.costs.co2_footprint == costs['co2_footprint']

    uuid = material_as_dict.pop('uuid')
    assert str(mat_from_dict.uuid) == uuid

    add_props = material_as_dict.pop('additional_properties')
    assert mat_from_dict.additional_properties[0].name == add_props[0]['name']
    assert mat_from_dict.additional_properties[0].value == add_props[0]['value']

    for k, v in material_as_dict.items():
        assert getattr(mat_from_dict, k) == v


def test_aggregates_to_dict():
    aggregates, aggregates_as_dict = _create_aggregates_material()

    for k, v in AggregatesStrategy.convert_material_to_dict(aggregates).items():
        if k in aggregates_as_dict.keys():
            assert aggregates_as_dict[k] == v


def test_aggregates_from_dict():
    _, gen_mat_as_dict = _create_generic_material()
    aggregates, aggregates_as_dict = _create_aggregates_material()

    full_aggregates_as_dict = gen_mat_as_dict | aggregates_as_dict

    aggregates_from_dict = AggregatesStrategy.create_material_from_dict(full_aggregates_as_dict)

    comp_as_dict = aggregates_as_dict.pop('composition')
    assert aggregates_from_dict.composition.fine_aggregates == comp_as_dict['fine_aggregates']
    assert aggregates_from_dict.composition.coarse_aggregates == comp_as_dict['coarse_aggregates']

    for k, v in aggregates_as_dict.items():
        assert getattr(aggregates_from_dict, k) == v


def test_powder_to_dict():
    powder, powder_as_dict = _create_powder_material()

    for k, v in PowderStrategy.convert_material_to_dict(powder).items():
        if k in powder_as_dict.keys():
            assert powder_as_dict[k] == v


def test_powder_from_dict():
    _, gen_mat_as_dict = _create_generic_material()
    powder, powder_as_dict = _create_powder_material()

    full_powder_as_dict = gen_mat_as_dict | powder_as_dict

    powder_from_dict = PowderStrategy.create_material_from_dict(full_powder_as_dict)

    comp_as_dict = powder_as_dict.pop('composition')
    assert powder_from_dict.composition.fe3_o2 == comp_as_dict['fe3_o2']
    assert powder_from_dict.composition.si_o2 == comp_as_dict['si_o2']

    struct_as_dict = powder_as_dict.pop('structure')
    assert powder_from_dict.structure.fine == struct_as_dict['fine']
    assert powder_from_dict.structure.gravity == struct_as_dict['gravity']

    for k, v in powder_as_dict.items():
        assert getattr(powder_from_dict, k) == v


def test_liquid_to_dict():
    liquid, liquid_as_dict = _create_liquid_material()

    for k, v in LiquidStrategy.convert_material_to_dict(liquid).items():
        if k in liquid_as_dict.keys():
            assert liquid_as_dict[k] == v


def test_liquid_from_dict():
    _, gen_mat_as_dict = _create_generic_material()
    liquid, liquid_as_dict = _create_liquid_material()

    full_liquid_as_dict = gen_mat_as_dict | liquid_as_dict

    liquid_from_dict = LiquidStrategy.create_material_from_dict(full_liquid_as_dict)

    comp_as_dict = liquid_as_dict.pop('composition')
    assert liquid_from_dict.composition.na2_si_o3 == comp_as_dict['na2_si_o3']
    assert liquid_from_dict.composition.na2_si_o3_mol == comp_as_dict['na2_si_o3_mol']

    for k, v in liquid_as_dict.items():
        assert getattr(liquid_from_dict, k) == v
