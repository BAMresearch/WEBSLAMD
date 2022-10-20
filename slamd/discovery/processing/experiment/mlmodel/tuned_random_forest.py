from mlxtend.feature_selection import SequentialFeatureSelector
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

from slamd.discovery.processing.experiment.mlmodel.slamd_random_forest import SlamdRandomForest


class TunedRandomForest:

    @classmethod
    def find_best_model(cls, training_rows, training_labels):
        sfs_rf_testing = SequentialFeatureSelector(estimator=SlamdRandomForest(),
                                                   forward=True,
                                                   floating=False,
                                                   scoring='r2',
                                                   cv=None)
        pipe = Pipeline([('sfs', sfs_rf_testing),
                        ('rf2', SlamdRandomForest())])
        grid_search_cv = GridSearchCV(estimator=pipe,
                                      param_grid=cls._create_parameters_for_grid_search(),
                                      scoring='r2',
                                      n_jobs=1,
                                      cv=4,
                                      refit=False)

        grid_search_cv = grid_search_cv.fit(training_rows, training_labels)
        # Return the best model found
        return pipe.set_params(**grid_search_cv.best_params_)

    @classmethod
    def _create_parameters_for_grid_search(cls):
        """
        Return the grid parameters required by GridSearchCV.
        Use 5 and 10 features. Use a max tree depth of 1 and 5.
        These hyperparameters were determined by performing some local experiments.
        In principle, these could be further tuned.
        """
        return {
            'sfs__k_features': [5, 10],
            'rf2__max_depth': [1, 5],
        }
