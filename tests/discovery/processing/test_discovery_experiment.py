import pandas as pd
import numpy as np

from slamd.discovery.processing.algorithms.discovery_experiment import DiscoveryExperiment


def test_clip_predictions_for_one_target_no_threshold():
    experiment = DiscoveryExperiment(
        pd.DataFrame({'x': []}), model="", curiosity=1, features=[], targets=['x'], target_weights=[1], target_thresholds=[None],
        target_max_or_min=['max'], apriori_thresholds=[], apriori_columns=[], apriori_weights=[],
        apriori_max_or_min=[]
    )

    input_prediction = np.arange(10).reshape(-1, 1)
    experiment.prediction = input_prediction

    clipped_prediction = experiment.clip_predictions()

    assert clipped_prediction.all() == input_prediction.all()
