from wtforms import ValidationError

from slamd.discovery.processing.discovery_persistence import DiscoveryPersistence


class DatasetNameIsUnique:
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        dataset_filename = field.data.filename
        dataset = DiscoveryPersistence.query_dataset_by_name(dataset_filename)
        if dataset:
            raise ValidationError(self.message)
