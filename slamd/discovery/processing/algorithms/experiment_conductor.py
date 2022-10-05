# Adapted from the original Sequential Learning App
# https://github.com/BAMresearch/SequentialLearningApp
import pandas as pd
from scipy.spatial import distance_matrix
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel

from slamd.common.error_handling import ValueNotSupportedException
from slamd.discovery.processing.algorithms.experiment_postprocessor import ExperimentPostprocessor
from slamd.discovery.processing.algorithms.experiment_preprocessor import ExperimentPreprocessor
from slamd.discovery.processing.algorithms.slamd_random_forest import SlamdRandomForest
from slamd.discovery.processing.models.model_type import ModelType


# Attention - suppressing expected Gaussian Regressor warnings
import warnings
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)


class ExperimentConductor:

    @classmethod
    def run(cls, exp):
        ExperimentPreprocessor.preprocess(exp)
        cls._fit_model_and_predict(exp)
        cls._calculate_utility(exp)
        cls._calculate_novelty(exp)

        return ExperimentPostprocessor.postprocess(exp)

    @classmethod
    def _fit_model_and_predict(cls, exp):
        if exp.model == ModelType.RANDOM_FOREST.value:
            regressor = SlamdRandomForest()
        elif exp.model == ModelType.GAUSSIAN_PROCESS.value:
            # Hyperparameters from Christoph
            kernel = ConstantKernel(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
            regressor = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9, random_state=42)
        else:
            raise ValueNotSupportedException(message=f'Invalid model: {exp.model}')

        predictions = {}
        uncertainties = {}
        for target in exp.target_names:
            # Train the model for every target with the corresponding rows and labels
            training_rows = exp.features_df.loc[exp.label_index].values
            training_labels = exp.targets_df.loc[exp.label_index, target].values.reshape(-1, 1)

            regressor.fit(training_rows, training_labels)

            # Predict the label for the remaining rows
            rows_to_predict = exp.features_df.loc[exp.nolabel_index].values
            prediction, uncertainty = regressor.predict(rows_to_predict, return_std=True)

            predictions[target] = prediction
            uncertainties[target] = uncertainty

        # Keep using old index to ensure compatibility between dataframes
        exp.prediction = pd.DataFrame(predictions, index=exp.nolabel_index)
        exp.uncertainty = pd.DataFrame(uncertainties, index=exp.nolabel_index)

    @classmethod
    def _calculate_utility(cls, exp):
        # The strategy is always 'MLI (explore & exploit)' for this implementation
        # See the original app for other possibilities

        prediction_for_utility, uncertainty_for_utility = cls._process_predictions(exp)
        apriori_for_utility = cls._process_apriori(exp)

        # Compute the value of the utility function
        # See slide 43 of the PowerPoint presentation
        exp.utility = apriori_for_utility + prediction_for_utility.sum(axis=1) + \
                      exp.curiosity * uncertainty_for_utility.sum(axis=1)

    @classmethod
    def _process_predictions(cls, exp):
        # Clip, norm, and weigh predictions for utility calculation
        # Targets which should be minimized instead of maximized are also inverted for the utility calculation

        # Clip
        clipped_prediction = cls.clip_prediction(exp)

        # Norm - use 1 as standard deviation instead of 0 to avoid division by 0 (unlikely)
        labels_std = exp.targets_df.loc[exp.label_index].std().replace(0, 1)
        labels_mean = exp.targets_df.loc[exp.label_index].mean()
        normed_uncertainty = exp.uncertainty / labels_std
        normed_prediction = (clipped_prediction - labels_mean) / labels_std

        # Invert
        for (column, value) in zip(exp.target_names, exp.target_max_or_min):
            if value == 'min':
                normed_prediction[column] *= (-1)

        # Weigh
        for (target, weight) in zip(exp.target_names, exp.target_weights):
            normed_prediction[target] *= weight
            normed_uncertainty[target] *= weight

        return normed_prediction, normed_uncertainty

    @classmethod
    def _process_apriori(cls, exp):
        # Norm, weigh and if necessary invert apriori columns for utility calculation

        if len(exp.apriori_names) == 0:
            return 0

        # Norm - use 1 as standard deviation instead of 0 to avoid division by 0
        normed_apriori_df = exp.apriori_df.copy()
        apriori_std = normed_apriori_df.std().replace(0, 1)
        apriori_mean = normed_apriori_df.mean()
        normed_apriori_df = (normed_apriori_df - apriori_mean) / apriori_std

        apriori_for_predicted_rows = normed_apriori_df.loc[exp.nolabel_index]

        # Weigh and invert
        for (col, weight, maxmin) in zip(exp.apriori_df.columns, exp.apriori_weights, exp.apriori_max_or_min):
            if maxmin == 'min':
                apriori_for_predicted_rows[col] *= weight * (-1)
            else:
                apriori_for_predicted_rows[col] *= weight

        return apriori_for_predicted_rows.sum(axis=1)

    @classmethod
    def _calculate_novelty(cls, exp):
        # Normalize first
        norm_features_df = exp.features_df.copy()
        features_std = norm_features_df.std().replace(0, 1)
        features_mean = norm_features_df.mean()
        norm_features_df = (norm_features_df - features_mean) / features_std

        features_of_predicted_rows = norm_features_df.loc[exp.nolabel_index]
        features_of_known_rows = norm_features_df.loc[exp.label_index]

        distance = distance_matrix(features_of_predicted_rows, features_of_known_rows)
        min_distances = distance.min(axis=1)
        max_of_min_distances = min_distances.max()

        novelty_as_array = min_distances * (max_of_min_distances ** (-1))

        exp.novelty = pd.DataFrame(
            {'Novelty': novelty_as_array},
            index=exp.nolabel_index
        )

    @classmethod
    def clip_prediction(cls, exp):
        clipped_prediction = exp.prediction.copy()
        for (target, max_or_min, threshold) in zip(exp.target_names, exp.target_max_or_min, exp.target_thresholds):
            if threshold is None:
                continue

            if max_or_min == 'min':
                clipped_prediction[target].clip(lower=threshold, inplace=True)
            elif max_or_min == 'max':
                clipped_prediction[target].clip(upper=threshold, inplace=True)

        return clipped_prediction
