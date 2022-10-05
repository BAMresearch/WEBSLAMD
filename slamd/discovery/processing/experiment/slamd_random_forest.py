import numpy as np
import pandas as pd
from lolopy.learners import RandomForestRegressor


LOLOPY_MINIMUM_DATA_POINTS = 8


class SlamdRandomForest(RandomForestRegressor):
    """
    Simple Wrapper for LolopyRandomForest implementation that automatically pads input to match the library's
    minimum data requirements
    """

    def fit(self, x, y, weights=None):
        if y.shape[0] < LOLOPY_MINIMUM_DATA_POINTS:
            x = np.tile(x, (4, 1))
            y = np.tile(y, (4, 1))

        y = pd.DataFrame(y)

        return super().fit(x, y, weights)

