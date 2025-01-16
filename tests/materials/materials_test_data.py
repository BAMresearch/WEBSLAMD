import slamd
from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.admixture import Admixture
from slamd.materials.processing.models.aggregates import Aggregates, Composition as AggregatesComposition
from slamd.materials.processing.models.liquid import Liquid
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.models.powder import Composition, Structure, Powder


# noinspection PyTypeChecker
def create_test_powders():
    composition = Composition(fe3_o2=23.3, si_o2=None)
    structure = Structure(fine=None, gravity=12)
    powder1 = Powder(
        name='test powder',
        type='Powder',
        composition=composition,
        structure=structure,
        additional_properties=[AdditionalProperty(
            name='test prop', value='test value')]
    )
    powder1.uuid = 'test uuid1'

    composition = Composition(fe3_o2=None, si_o2=None)
    structure = Structure(fine=None, gravity=None)
    powder2 = Powder(
        name='my powder',
        type='Powder',
        composition=composition,
        structure=structure,
        additional_properties=[]
    )
    powder2.uuid = 'test uuid2'
    return [powder1, powder2]


def create_test_aggregates():
    composition = AggregatesComposition(fine_aggregates=12)
    aggregates = Aggregates(
        name='test aggregate',
        type='Aggregates',
        composition=composition,
        additional_properties=[AdditionalProperty(
            name='aggregate property', value='aggregate property value')]
    )
    aggregates.uuid = 'test aggregate uuid'
    return [aggregates]


def prepare_test_base_powders_for_blending(material_type, uuid):
    if uuid == 'uuid1':
        powder1 = Powder(name='powder 1', type='Powder',
                         costs=Costs(co2_footprint=20, costs=50, delivery_time=30),
                         composition=slamd.materials.processing.models.powder.Composition(fe3_o2=10.0, si_o2=4.4,
                                                                                          al2_o3=7, na2_o=11),
                         structure=Structure(fine=50, gravity=10),
                         additional_properties=[AdditionalProperty(name='Prop1', value='2'),
                                                AdditionalProperty(name='Prop2', value='Category'),
                                                AdditionalProperty(name='Prop3', value='Not in powder 2'),
                                                AdditionalProperty(name='Prop4', value='12')])
        powder1.uuid = 'uuid1'
        return powder1
    if uuid == 'uuid2':
        powder2 = Powder(name='powder 2', type='Powder',
                         costs=Costs(co2_footprint=10, costs=30, delivery_time=40),
                         composition=slamd.materials.processing.models.powder.Composition(fe3_o2=20.0, al2_o3=7,
                                                                                          si_o2=10),
                         structure=Structure(fine=100),
                         additional_properties=[AdditionalProperty(name='Prop1', value='4'),
                                                AdditionalProperty(name='Prop2', value='Other Category'),
                                                AdditionalProperty(name='Prop4', value='No Number')])
        powder2.uuid = 'uuid2'
        return powder2
    if uuid == 'uuid3':
        powder1 = Powder(name='powder 3', type='Powder',
                         costs=Costs(co2_footprint=20, costs=50, delivery_time=30),
                         composition=slamd.materials.processing.models.powder.Composition(fe3_o2=10.0, si_o2=4.4,
                                                                                          al2_o3=7, na2_o=11),
                         structure=Structure(fine=50, gravity=10),
                         additional_properties=[AdditionalProperty(name='Prop1', value='10'),
                                                AdditionalProperty(name='Prop2', value='Category'),
                                                AdditionalProperty(name='Prop3', value='Not in powder 2'),
                                                AdditionalProperty(name='Prop4', value='10.2')])
        powder1.uuid = 'uuid3'
        return powder1
    return None


def prepare_test_base_aggregates_for_blending(material_type, uuid):
    if uuid == 'uuid1':
        aggregates1 = Aggregates(name='aggregate 1', type='Aggregates',
                                 costs=Costs(co2_footprint=20, costs=50, delivery_time=30),
                                 composition=slamd.materials.processing.models.aggregates.Composition(
                                     fine_aggregates=10.0, coarse_aggregates=4.4, gravity=7,
                                     fineness_modulus=5, water_absorption=10),
                                 additional_properties=[AdditionalProperty(name='Prop1', value='2'),
                                                        AdditionalProperty(name='Prop2', value='Category'),
                                                        AdditionalProperty(name='Prop3', value='Not a number 1')])
        aggregates1.uuid = 'uuid1'
        return aggregates1
    if uuid == 'uuid2':
        aggregates2 = Aggregates(name='aggregate 2', type='Aggregates',
                                 costs=Costs(co2_footprint=10, costs=30, delivery_time=40),
                                 composition=slamd.materials.processing.models.aggregates.Composition(
                                     fine_aggregates=20.0, coarse_aggregates=4.1, gravity=4,
                                     fineness_modulus=5, water_absorption=10),
                                 additional_properties=[AdditionalProperty(name='Prop1', value='5'),
                                                        AdditionalProperty(name='Prop2', value='Category'),
                                                        AdditionalProperty(name='Prop3', value='12')])
        aggregates2.uuid = 'uuid2'
        return aggregates2
    if uuid == 'uuid3':
        aggregates3 = Aggregates(name='aggregate 3', type='Aggregates',
                                 costs=Costs(co2_footprint=70, costs=20, delivery_time=40),
                                 composition=slamd.materials.processing.models.aggregates.Composition(
                                     fine_aggregates=27.0, coarse_aggregates=9.0, gravity=6,
                                     fineness_modulus=5, water_absorption=10),
                                 additional_properties=[AdditionalProperty(name='Prop1', value='5'),
                                                        AdditionalProperty(name='Prop2', value='Other Category'),
                                                        AdditionalProperty(name='Prop3', value='Not a number 2')])
        aggregates3.uuid = 'uuid3'
        return aggregates3
    return None


def prepare_test_base_liquids_for_blending(material_type, uuid):
    if uuid == 'uuid1':
        liquid1 = Liquid(name='liquid 1', type='Liquid',
                         costs=Costs(co2_footprint=20, costs=50, delivery_time=30),
                         composition=slamd.materials.processing.models.liquid.Composition(
                             na2_si_o3=10.0, na_o_h=4.4, na2_si_o3_mol=7,
                             h2_o_mol=11),
                         additional_properties=[AdditionalProperty(name='Prop1', value='2'),
                                                AdditionalProperty(name='Prop2', value='Category'),
                                                AdditionalProperty(name='Prop3', value='Not a liquid 1')])
        liquid1.uuid = 'uuid1'
        return liquid1
    if uuid == 'uuid2':
        liquid2 = Liquid(name='liquid 2', type='Liquid',
                         costs=Costs(co2_footprint=10, costs=30, delivery_time=40),
                         composition=slamd.materials.processing.models.liquid.Composition(
                             na2_si_o3=20.0, na_o_h=4.1, na2_si_o3_mol=4,
                             h2_o_mol=11),
                         additional_properties=[AdditionalProperty(name='Prop1', value='5'),
                                                AdditionalProperty(name='Prop2', value='Category'),
                                                AdditionalProperty(name='Prop3', value='12')])
        liquid2.uuid = 'uuid2'
        return liquid2
    if uuid == 'uuid3':
        liquid3 = Liquid(name='liquid 3', type='Liquid',
                         costs=Costs(co2_footprint=70, costs=20, delivery_time=40),
                         composition=slamd.materials.processing.models.liquid.Composition(
                             na2_si_o3=27.0, na_o_h=9.0, na2_si_o3_mol=6,
                             h2_o_mol=16),
                         additional_properties=[AdditionalProperty(name='Prop1', value='5'),
                                                AdditionalProperty(name='Prop2', value='Other Category'),
                                                AdditionalProperty(name='Prop3', value='Not a liquid 2')])
        liquid3.uuid = 'uuid3'
        return liquid3
    return None


def prepare_test_admixture():
    aggregates1 = Admixture(name='admixture 1', type='Admixture',
                            costs=Costs(co2_footprint=11, costs=55, delivery_time=31),
                            additional_properties=[])
    aggregates1.uuid = 'uuid admixture'
    return aggregates1
