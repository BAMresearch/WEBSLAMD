import slamd
from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.aggregates import Aggregates, Composition as AggregatesComposition
from slamd.materials.processing.models.powder import Composition, Structure, Powder


def create_test_powders():
    composition = Composition(fe3_o2='23.3', si_o2=None)
    structure = Structure(fine=None, gravity='12')
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
