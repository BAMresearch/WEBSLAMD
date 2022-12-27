from dataclasses import dataclass
from pandas import DataFrame
from slamd.discovery.processing.add_targets_dto import DataWithTargetsDto
from slamd.discovery.processing.forms.extend_form import ExtendForm
from slamd.discovery.processing.forms.targets_form import TargetsForm


@dataclass
class ExtendPageData:
    dataframe: DataFrame = None
    # string_columns: list[str] = None
    extend_form: ExtendForm = None
