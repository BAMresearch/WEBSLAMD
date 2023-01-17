from dataclasses import dataclass

from pandas import DataFrame

from slamd.discovery.processing.forms.extend_form import ExtendForm


@dataclass
class ExtendPageData:
    dataframe: DataFrame = None
    extend_form: ExtendForm = None


