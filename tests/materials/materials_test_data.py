import slamd
from slamd.materials.processing.models.additional_property import AdditionalProperty
from slamd.materials.processing.models.aggregates import Aggregates
from slamd.materials.processing.models.powder import Structure, Powder


def create_test_powders():
    powder1 = Powder(slamd.materials.processing.models.powder.Composition(fe3_o2='23.3', si_o2=None),
                     slamd.materials.processing.models.powder.Structure(fine=None, gravity='12'))
    powder1.uuid = 'test uuid1'
    powder1.name = 'test powder'
    powder1.type = 'Powder'
    powder1.additional_properties = [
        AdditionalProperty(name='test prop', value='test value')]
    powder2 = Powder(slamd.materials.processing.models.powder.Composition(fe3_o2=None, si_o2=None),
                     slamd.materials.processing.models.powder.Structure(fine=None, gravity=None))
    powder2.uuid = 'test uuid2'
    powder2.name = 'my powder'
    powder2.type = 'Powder'
    powder2.additional_properties = []
    return [powder1, powder2]


def create_test_aggregates():
    aggregates = Aggregates(slamd.materials.processing.models.aggregates.Composition(fine_aggregates=12))
    aggregates.uuid = 'test aggregate uuid'
    aggregates.name = 'test aggregate'
    aggregates.type = 'Aggregates'
    aggregates.additional_properties = [
        AdditionalProperty(name='aggregate property', value='aggregate property value')]
    return [aggregates]
