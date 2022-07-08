import slamd
from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.aggregates import Aggregates, Composition as AggregatesComposition
from slamd.materials.processing.models.powder import Composition, Structure, Powder


def create_test_powders():
    composition = Composition(fe3_o2='23.3', si_o2=None)
    structure = Structure(fine=None, gravity='12')
    powder1 = Powder(composition=composition, structure=structure)
    powder1.uuid = 'test uuid1'
    powder1.name = 'test powder'
    powder1.type = 'Powder'
    powder1.additional_properties = [
        AdditionalProperty(name='test prop', value='test value')]

    composition = Composition(fe3_o2=None, si_o2=None)
    structure = Structure(fine=None, gravity=None)
    powder2 = Powder(composition=composition, structure=structure)
    powder2.uuid = 'test uuid2'
    powder2.name = 'my powder'
    powder2.type = 'Powder'
    powder2.additional_properties = []
    return [powder1, powder2]


def create_test_aggregates():
    composition = AggregatesComposition(fine_aggregates=12)
    aggregates = Aggregates(composition=composition)
    aggregates.uuid = 'test aggregate uuid'
    aggregates.name = 'test aggregate'
    aggregates.type = 'Aggregates'
    aggregates.additional_properties = [
        AdditionalProperty(name='aggregate property', value='aggregate property value')]
    return [aggregates]
