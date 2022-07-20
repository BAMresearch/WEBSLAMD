from slamd.materials.processing.models.aggregates import Aggregates, Composition
from slamd.materials.processing.ratio_parser import RatioParser
from slamd.materials.processing.strategies.base_material_strategy import MaterialStrategy
from slamd.materials.processing.strategies.blending_properties_calculator import BlendingPropertiesCalculator


class AggregatesStrategy(MaterialStrategy):

    def create_model(self, submitted_material):
        composition = Composition(
            fine_aggregates=submitted_material['fine_aggregates'],
            coarse_aggregates=submitted_material['coarse_aggregates'],
            fa_density=submitted_material['fa_density'],
            ca_density=submitted_material['ca_density']
        )

        return Aggregates(
            name=submitted_material['material_name'],
            type=submitted_material['material_type'],
            costs=self.extract_cost_properties(submitted_material),
            composition=composition,
            additional_properties=self.extract_additional_properties(submitted_material)
        )

    def gather_composition_information(self, aggregates):
        return [self.include('Fine Aggregates', aggregates.composition.fine_aggregates),
                self.include('Coarse Aggregates', aggregates.composition.coarse_aggregates),
                self.include('FA Density', aggregates.composition.fa_density),
                self.include('CA Density', aggregates.composition.ca_density)]

    def convert_to_multidict(self, aggregates):
        multidict = super().convert_to_multidict(aggregates)
        multidict.add('fine_aggregates', aggregates.composition.fine_aggregates)
        multidict.add('coarse_aggregates', aggregates.composition.coarse_aggregates)
        multidict.add('fa_density', aggregates.composition.fa_density)
        multidict.add('ca_density', aggregates.composition.ca_density)
        return multidict

    def create_blended_material(self, idx, blended_material_name, normalized_ratios, base_aggregates_as_dict):
        costs = self.compute_blended_costs(normalized_ratios, base_aggregates_as_dict)
        composition = self._compute_blended_composition(normalized_ratios, base_aggregates_as_dict)
        additional_properties = self.compute_additional_properties(normalized_ratios, base_powders_as_dict)

        return Aggregates(type=base_aggregates_as_dict[0]['type'],
                          name=f'{blended_material_name}-{idx}',
                          costs=costs,
                          composition=composition,
                          additional_properties=additional_properties,
                          is_blended=True,
                          blending_ratios=RatioParser.ratio_list_to_ratio_string(normalized_ratios))

    def _compute_blended_composition(self, normalized_ratios, base_powders_as_dict):
        blended_fine_aggregates = BlendingPropertiesCalculator.compute_mean(normalized_ratios, base_powders_as_dict,
                                                                            'composition', 'fine_aggregates')
        blended_coarse_aggregates = BlendingPropertiesCalculator.compute_mean(normalized_ratios, base_powders_as_dict,
                                                                              'composition', 'coarse_aggregates')
        blended_fa_density = BlendingPropertiesCalculator.compute_mean(normalized_ratios, base_powders_as_dict,
                                                                       'composition', 'fa_density')
        blended_ca_density = BlendingPropertiesCalculator.compute_mean(normalized_ratios, base_powders_as_dict,
                                                                       'composition', 'ca_density')

        composition = Composition(fine_aggregates=blended_fine_aggregates, coarse_aggregates=blended_coarse_aggregates,
                                  fa_density=blended_fa_density, ca_density=blended_ca_density)

        return composition
