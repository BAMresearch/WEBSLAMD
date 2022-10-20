import numpy as np
import pandas as pd
from lolopy.learners import RandomForestRegressor


LOLOPY_MINIMUM_DATA_POINTS = 8


class SlamdRandomForest(RandomForestRegressor):
    """
    Simple Wrapper for LolopyRandomForest implementation that automatically pads input to match the library's
    minimum data requirements
    """

    def fit(self, X, y, weights=None, random_seed=42):
        if y.shape[0] < LOLOPY_MINIMUM_DATA_POINTS:
            X = np.tile(X, (4, 1))
            y = np.tile(y, (4, 1))

        y = pd.DataFrame(y)

        return super().fit(X, y, weights, random_seed)
