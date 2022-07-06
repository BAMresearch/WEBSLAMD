class BaseMaterialDto:

    def __init__(self, uuid='', name='', type='', all_properties=''):
        self.uuid = uuid
        self.type = type
        self.name = name
        self.all_properties = all_properties
