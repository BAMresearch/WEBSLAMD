from abc import ABC, abstractmethod

from slamd.common.slamd_utils import empty


class BaseMaterialStrategy(ABC):

    @abstractmethod
    def create_model(self, submitted_material, additional_properties):
        pass

    @abstractmethod
    def create_dto(self, material):
        pass

    def _include(self, displayed_name, property):
        if empty(property):
            return ''
        return f' {displayed_name}: {property},'
