from functools import reduce
from itertools import product

from slamd.common.slamd_utils import empty
from slamd.materials.processing.materials_facade import MaterialsFacade


class WeightsCalculator:

    @classmethod
    def compute_cartesian_product(cls, all_materials_weights):
        cartesian_product_of_independent_weights = product(*all_materials_weights)
        cartesian_product_list_of_independent_weights = list(cartesian_product_of_independent_weights)
        return cartesian_product_list_of_independent_weights

    @classmethod
    def compute_full_cartesian_product(cls, all_materials_weights, materials_formulation_configuration,
                                       weight_constraint):
        cartesian_product_list_of_independent_weights = WeightsCalculator.compute_cartesian_product(
            all_materials_weights)
        full_cartesian_product = []
        for item in cartesian_product_list_of_independent_weights:

            dependent_material = cls._find_dependent_material(materials_formulation_configuration)
            blending_ratios = dependent_material.blending_ratios

            entry_list = list(item)
            dependent_weight = cls._compute_dependent_weight(entry_list, weight_constraint)

            # if statement: dependent material is itself a base material
            if empty(blending_ratios):
                entry_list.append(str(dependent_weight))

            # else statement: dependent material is a blended material
            else:
                dependent_weight_ratios = ''
                ratios = blending_ratios.split('/')
                for ratio in ratios:
                    dependent_weight_ratios += f'{round(float(ratio) * float(dependent_weight), 2)}/'
                dependent_weight_ratios = dependent_weight_ratios.strip()[:-1]
                entry_list.append(dependent_weight_ratios)

            full_cartesian_product.append(entry_list)

        return full_cartesian_product

    @classmethod
    def _find_dependent_material(cls, materials_formulation_configuration):
        index_of_dependent_material = len(materials_formulation_configuration) - 1
        dependent_material_uuid = materials_formulation_configuration[index_of_dependent_material]['uuid']
        dependent_material_type = materials_formulation_configuration[index_of_dependent_material]['type']
        dependent_material = MaterialsFacade.get_material(dependent_material_type, dependent_material_uuid)
        return dependent_material

    @classmethod
    def _compute_dependent_weight(cls, entry_list, weight_constraint):
        sum_of_all = 0
        dependent_weight = weight_constraint
        for ratios in entry_list:
            pieces = ratios.split('/')
            if len(pieces) == 0:
                sum_of_all += float(ratios[0])
            else:
                sum_of_all += float(reduce(lambda x, y: float(x) + float(y), pieces))
            dependent_weight = (round(float(weight_constraint) - sum_of_all, 2))
        return dependent_weight
