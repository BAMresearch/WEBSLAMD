from flask import session

from slamd.materials.model.base_material import Costs
from slamd.materials.model.powder import Powder, Composition, Structure


class PowderStrategy:

    def create_model(self, submitted_material, additional_properties):
        composition = Composition()
        composition.feo = submitted_material['feo']
        composition.sio = submitted_material['sio']

        costs = Costs()
        costs.co2_footprint = submitted_material['co2_footprint']
        costs.delivery_time = submitted_material['delivery_time']
        costs.costs = submitted_material['costs']

        structure = Structure()
        structure.gravity = submitted_material['gravity']
        structure.fine = submitted_material['fine']

        powder = Powder()

        powder.name = submitted_material['material_name']
        powder.type = submitted_material['material_type']
        powder.costs = costs
        powder.composition = composition
        powder.structure = structure
        powder.additional_properties = additional_properties

        before = session.get('powder_list', None)

        if before is None:
            session['powder_list'] = [powder]
        else:
            session['powder_list'].append(powder)
