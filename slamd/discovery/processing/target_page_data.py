from dataclasses import dataclass
from pandas import DataFrame
from slamd.discovery.processing.add_targets_dto import DataWithTargetsDto
from slamd.discovery.processing.forms.targets_form import TargetsForm


@dataclass
class TargetPageData:
    dataframe: DataFrame = None
    all_dtos: list[DataWithTargetsDto] = None
    target_name_list: list[str] = None
    targets_form: TargetsForm = None
