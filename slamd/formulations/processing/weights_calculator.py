from functools import reduce
from itertools import product

from slamd.materials.processing.materials_facade import MaterialsFacade


class WeightsCalculator:

    @classmethod
    def compute_full_concrete_weights_product(cls, all_materials_weights, weight_constraint):
        independent_weights_product = cls._compute_independent_weights_product_for_concrete(all_materials_weights)

        full_weights_product = []

        for item in independent_weights_product:
            entry_list = list(item)
            dependent_weight = cls._compute_dependent_concrete_weight(entry_list, weight_constraint)

            entry_list.append(str(dependent_weight))
            full_weights_product.append(entry_list)

        return full_weights_product

    @classmethod
    def compute_full_binder_weights_product(cls, all_materials_weights, weight_constraint):
        independent_weights_product = cls._compute_independent_weights_data_product_for_binder(all_materials_weights)

        full_weights_product = []

        for item in independent_weights_product:
            entry_list = list(item)
            dependent_weight = cls._compute_dependent_binder_weight(entry_list, weight_constraint)

            entry_list[0] = str(round(float(entry_list[0]) * dependent_weight, 2))

            entry_list.append(str(dependent_weight))
            full_weights_product.append(entry_list)

        return full_weights_product

    @classmethod
    def _compute_independent_weights_product_for_concrete(cls, all_materials_weights):
        # "independent" is a slight misnomer as the liquid weights are defined in relation to the powder weights
        # However, they are independent in the sense that they do not depend on the mass constraint
        powder_weights = all_materials_weights[0]
        liquid_weight_ratios = all_materials_weights[1]
        remaining_weights = all_materials_weights[:]

        weights_product = []

        for pw in powder_weights:
            # They're strings - cast to float for multiplication, round, then cast back to string
            liquid_weights = [str(round(float(lwr) * float(pw), 2)) for lwr in liquid_weight_ratios]
            weights_product += list(product([pw], liquid_weights, *remaining_weights))

        return weights_product

    @classmethod
    def _compute_independent_weights_data_product_for_binder(cls, all_materials_weights):
        liquid_weight_ratios = all_materials_weights[0]
        remaining_weights = all_materials_weights[1:len(all_materials_weights)]

        return list(product(liquid_weight_ratios, *remaining_weights))

    @classmethod
    def _compute_dependent_concrete_weight(cls, entry_list, weight_constraint):
        sum_of_all = 0
        dependent_weight = weight_constraint
        for ratios in entry_list:
            pieces = ratios.split('/')
            if len(pieces) == 0:
                sum_of_all += float(ratios[0])
            else:
                sum_of_all += sum([float(piece) for piece in pieces])
            dependent_weight = (round(float(weight_constraint) - sum_of_all, 2))
        return dependent_weight

    @classmethod
    def _compute_dependent_binder_weight(cls, entry_list, weight_constraint):
        non_powder_or_liquid_masses = [float(w) for w in entry_list[1:]]
        powder_mass = (float(weight_constraint) - sum(non_powder_or_liquid_masses)) / (1 + float(entry_list[0]))
        return round(powder_mass, 2)

    @classmethod
    def compute_weights_from_ratios(cls, all_materials_weights_and_ratios,admixture_custom_indices):
        powder_weights = all_materials_weights_and_ratios[0]
        liquid_ratios = all_materials_weights_and_ratios[1]
        admixture_ratios = []
        liquid_weights = []
        admixture_weights = []

        if admixture_custom_indices.get('admixture_index'):
            admixture_ratios = all_materials_weights_and_ratios[admixture_custom_indices['admixture_index']]

        for powder_weight in powder_weights:
            for liquid_ratio in liquid_ratios:
                liquid_weights.append(float(powder_weight) * float(liquid_ratio) / 100)
            for admixture_ratio in admixture_ratios:
                admixture_weights.append(float(powder_weight) * float(admixture_ratio) / 100)

        all_materials_weights_and_ratios[1] = [str(val) for val in liquid_weights]
        all_materials_weights_and_ratios[2] = [str(val) for val in admixture_weights]

        return all_materials_weights_and_ratios

