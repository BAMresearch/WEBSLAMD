from mlxtend.feature_selection import SequentialFeatureSelector
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline


class TunedGaussianProcessRegressor:

    @classmethod
    def find_best_model(cls, training_rows, training_labels):
        sfs_gr_testing = SequentialFeatureSelector(estimator=cls._create_baseline_gpr_for_further_tuning(),
                                                   forward=True,
                                                   floating=False,
                                                   scoring='r2',
                                                   cv=None)
        pipe = Pipeline([('sfs', sfs_gr_testing),
                         ('gp2', cls._create_baseline_gpr_for_further_tuning())])
        grid_search_cv = GridSearchCV(estimator=pipe,
                                      param_grid=cls._create_parameters_for_grid_search(),
                                      scoring='r2',
                                      n_jobs=-1,
                                      cv=4,
                                      refit=False)
        grid_search_cv = grid_search_cv.fit(training_rows, training_labels)
        # Return the best model found
        return pipe.set_params(**grid_search_cv.best_params_)

    @classmethod
    def _create_baseline_gpr_for_further_tuning(cls):
        """
        Return a Gaussian Process Regressor with hyperparameters normalize_y=True, n_restarts_optimizer=3
        These hyperparameters were found in previous experiments to works best.
        n_restarts_optimizer=3 is a compromise between speed and predictive power.
        """
        return GaussianProcessRegressor(normalize_y=True, n_restarts_optimizer=3, random_state=42)

    @classmethod
    def _create_anisotropic_kernel(cls, n_dims):
        return ConstantKernel(1.0, constant_value_bounds='fixed') * RBF(length_scale=[1] * n_dims)

    @classmethod
    def _create_parameters_for_grid_search(cls):
        """
        Return the grid parameters required by GridSearchCV.
        Use an isotropic and an anisotropic kernel.
        Use 5 and 10 features respectively for the anisotropic kernel.
        These hyperparameters were determined by performing some local experiments.
        In principle, these could be further tuned.
        """
        default_kernel = ConstantKernel(1.0, constant_value_bounds='fixed') * RBF(1.0, length_scale_bounds='fixed')
        return [
            {
                'sfs__k_features': [5],
                'sfs__estimator__kernel': [default_kernel],
                'gp2__kernel': [default_kernel, cls._create_anisotropic_kernel(5)]
            },
            {
                'sfs__k_features': [10],
                'sfs__estimator__kernel': [default_kernel],
                'gp2__kernel': [default_kernel, cls._create_anisotropic_kernel(10)]
            }
        ]
