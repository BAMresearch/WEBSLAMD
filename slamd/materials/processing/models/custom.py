from slamd.materials.processing.models.material import Material


class Custom(Material):

    def __init__(self, name='', type='', costs=None, custom_name=None, custom_value=None, additional_properties=None):
        super().__init__(name=name, type=type, costs=None)
        self.custom_name = custom_name
        self.custom_value = custom_value
        self.additional_properties = additional_properties
