from slamd.materials.processing.models.liquid import Liquid, Composition
from slamd.materials.processing.models.material import Costs
from slamd.materials.processing.strategies.liquid_strategy import LiquidStrategy


def test_gather_composition_properties_adds_all_properties():
    strategy = LiquidStrategy()
    composition = Composition(
        na2_si_o3=12.3,
        na_o_h=23.4,
        na2_si_o3_specific=34.5,
        na_o_h_specific=45.6,
        total=56.7,
        na2_o=67.8,
        si_o2=78.9,
        h2_o=89.0,
        na2_o_dry=0.98,
        si_o2_dry=9.87,
        water=8.76,
        na_o_h_total=7.65
    )
    liquid = Liquid(
        name='test liquid',
        type='Liquid',
        costs=Costs(),
        additional_properties=[],
        composition=composition
    )

    result = strategy.gather_composition_information(liquid)
    assert result == ['Na₂SiO₃: 12.3, ',
                      'NaOH: 23.4, ',
                      'Na₂SiO₃ specific: 34.5, ',
                      'NaOH specific: 45.6, ',
                      'Total solution: 56.7, ',
                      'Na₂O: 67.8, ',
                      'SiO₂: 78.9, ',
                      'H₂O: 89.0, ',
                      'Na₂O: 0.98, ',
                      'SiO₂: 9.87, ',
                      'Water: 8.76, ',
                      'Total NaOH: 7.65, ']
