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
        utility = cls._calculate_utility(exp)
        novelty = cls._calculate_novelty(exp)

        return ExperimentPostprocessor.postprocess(exp, utility, novelty)

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
            training_labels = exp.targets_df.loc[exp.label_index, target].values

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

        normed_prediction, normed_uncertainty = cls._process_predictions(exp)

        # Normalize feature data
        # TODO Discuss this function
        cls._normalize_data(exp)

        # Apply weights to apriori values
        weighted_apriori_values_for_predicted_rows = cls._apply_weights_and_maxmin_to_apriori_values(exp)

        # Compute the value of the utility function
        # See slide 43 of the PowerPoint presentation
        utility = weighted_apriori_values_for_predicted_rows + normed_prediction.sum(axis=1) + \
                  exp.curiosity * normed_uncertainty.sum(axis=1)

        return utility

    @classmethod
    def _process_predictions(cls, exp):
        # Clip, norm, and weigh predictions for utility calculation
        # Targets which should be minimized instead of maximized are also inverted for the utility calculation

        # Clip
        clipped_prediction = cls.clip_prediction(exp)

        # Sanity check TODO keep?
        assert all([x == y for x, y in zip(clipped_prediction, exp.target_names)])

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
    def _calculate_novelty(cls, exp):
        features_of_predicted_rows = exp.features_df.loc[exp.nolabel_index]
        features_of_known_rows = exp.features_df.loc[exp.label_index]

        distance = distance_matrix(features_of_predicted_rows, features_of_known_rows)
        min_distances = distance.min(axis=1)
        max_of_min_distances = min_distances.max()

        return min_distances * (max_of_min_distances ** (-1))

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

    @classmethod
    def _normalize_data(cls, exp):
        # TODO What about categoricals? => double check
        # replace 0s with 1s for division
        # print()
        # print(exp.dataframe[sorted(list(exp.dataframe.columns))].to_string())
        std = exp.dataframe.std().replace(0, 1)
        exp.dataframe = (exp.dataframe - exp.dataframe.mean()) / std
        # print(exp.dataframe[sorted(list(exp.dataframe.columns))].to_string())

    @classmethod
    def _apply_weights_and_maxmin_to_apriori_values(cls, exp):
        if len(exp.apriori_names) == 0:
            return 0

        apriori_for_predicted_rows = exp.apriori_df.loc[exp.nolabel_index].copy()

        for (col, weight, maxmin) in zip(exp.apriori_df.columns, exp.apriori_weights, exp.apriori_max_or_min):
            if maxmin == 'min':
                apriori_for_predicted_rows[col] *= weight * (-1)
            else:
                apriori_for_predicted_rows[col] *= weight

        return apriori_for_predicted_rows.sum(axis=1)
