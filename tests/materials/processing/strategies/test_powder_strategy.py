from slamd.materials.processing.models.powder import Powder, Structure, Composition
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.powder_strategy import PowderStrategy


def test_gather_composition_properties_adds_all_properties():
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
        mn2_o3=7.65
    )
    structure = Structure(
        fine=123.45,
        gravity=678.90
    )
    powder = Powder(
        name='test powder',
        type='Powder',
        costs=Costs(),
        additional_properties=[],
        composition=composition,
        structure=structure
    )

    result = PowderStrategy.gather_composition_information(powder)
    assert result == ['Fe₂O₃: 12.3, ',
                      'SiO₂: 23.4, ',
                      'Al₂O₃: 34.5, ',
                      'CaO: 45.6, ',
                      'MgO: 56.7, ',
                      'Na₂O: 67.8, ',
                      'K₂O: 78.9, ',
                      'SO₃: 89.0, ',
                      'TiO₂: 0.98, ',
                      'P₂O₅: 9.87, ',
                      'SrO: 8.76, ',
                      'Mn₂O₃: 7.65, ',
                      'Fine modules: 123.45, ',
                      'Specific gravity: 678.9, ']
