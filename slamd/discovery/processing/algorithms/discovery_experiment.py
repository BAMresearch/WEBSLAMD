# Adapted from the original Sequential Learning App
# https://github.com/BAMresearch/SequentialLearningApp
import numpy as np
import pandas as pd
from lolopy.learners import RandomForestRegressor
from scipy.spatial import distance_matrix
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel
from sklearn.preprocessing import OrdinalEncoder

from slamd.common.error_handling import ValueNotSupportedException, SequentialLearningException
from slamd.discovery.processing.algorithms.experiment_preprocessor import ExperimentPreprocessor
from slamd.discovery.processing.algorithms.plot_generator import PlotGenerator


class DiscoveryExperiment:

    @classmethod
    def run(cls, exp):
        ExperimentPreprocessor.preprocess(exp)

        cls.fit_model(exp)

        # self._encode_categoricals()
        # self.decide_max_or_min(self.target_df, self.targets, self.target_max_or_min)
        # self.decide_max_or_min(self.apriori_df, self.apriori_columns, self.apriori_max_or_min)
        # self.fit_model()

        # The strategy is always 'MLI (explore & exploit)' for this implementation
        # See the original app for other possibilities
        utility_function = self.update_index_MLI()

        novelty_factor = self.compute_novelty_factor()

        # Original dataframe
        df = self.dataframe
        # Add the columns with utility and novelty values
        df = df.iloc[self.prediction_index].assign(Utility=pd.Series(utility_function).values)
        df = df.loc[self.prediction_index].assign(Novelty=pd.Series(novelty_factor).values)

        # Fill in prediction and uncertainty values
        if self.uncertainty.ndim > 1:
            for i in range(len(self.targets)):
                df[self.targets[i]] = self.prediction[:, i]
                uncertainty_name_column = f'Uncertainty ({self.targets[i]})'
                df[uncertainty_name_column] = self.uncertainty[:, i].tolist()
                df[uncertainty_name_column] = df[uncertainty_name_column].apply(lambda row: round(row, 5))
        else:
            df[self.targets] = self.prediction.reshape(len(self.prediction), 1)
            uncertainty_name_column = f'Uncertainty ({self.targets[0]})'
            df[uncertainty_name_column] = self.uncertainty.reshape(len(self.uncertainty), 1)
            df[uncertainty_name_column] = df[uncertainty_name_column].apply(lambda row: round(row, 5))

        df[self.targets] = df[self.targets].apply(lambda row: round(row, 6))
        df['Utility'] = df['Utility'].apply(lambda row: round(row, 6))
        df['Novelty'] = df['Novelty'].apply(lambda row: round(row, 6))

        sorted = df.sort_values(by='Utility', ascending=False)
        # Number the rows from 1 to n (length of the dataframe) to identify them easier on the plots.
        sorted.insert(loc=0, column='Row number', value=[i for i in range(1, len(sorted) + 1)])

        columns_for_plot = self.targets.copy()
        columns_for_plot.extend(['Utility', 'Row number'])
        if len(self.apriori_columns) > 0:
            columns_for_plot.extend(self.apriori_columns)

        candidate_or_target = ['candidate' if row in self.sample_index else 'target' for row in self.features_df.index]

        scatter_plot = PlotGenerator.create_target_scatter_plot(sorted[columns_for_plot])
        tsne_plot = PlotGenerator.create_tsne_input_space_plot(self.features_df, candidate_or_target)

        return sorted, scatter_plot, tsne_plot

    @classmethod
    def fit_model(cls, exp):
        if exp.model == 'AI Model (lolo Random Forest)':
            cls.fit_random_forest_with_jack_knife_variance_estimators(exp)
        elif exp.model == 'Statistics-based model (Gaussian Process Regression)':
            cls.fit_gaussian_process_regression(exp)
        else:
            raise ValueNotSupportedException(f'Model {exp.model} value not supported')

    @classmethod
    def fit_gaussian_process_regression(cls, exp):
        for i, target in enumerate(exp.target_names):
            # Initialize the model with given hyperparameters
            kernel = ConstantKernel(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
            gpr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9, random_state=42)

            # Train the GPR model for every target with the corresponding rows and labels

            training_rows = exp.features_df.loc[exp.label_index].values
            training_labels = exp.targets_df.loc[exp.sample_index, target].values

            cls._check_target_label_validity(training_labels, exp)

            # TODO this should be checked during preprocessing
            # nan_counts = list(self.target_df.isna().sum())
            #
            # previous_count = nan_counts[0]
            # for j in range(1, len(nan_counts)):
            #     if nan_counts[1] != previous_count:
            #         raise SequentialLearningException('Targets used are labelled for differing rows.')
            #     previous_count = nan_counts[j]

            gpr.fit(training_rows, training_labels)

            # Predict the label for the remaining rows
            rows_to_predict = exp.features_df.loc[exp.nolabel_index]
            prediction, uncertainty = gpr.predict(rows_to_predict, return_std=True)

            if i == 0:
                uncertainty_stacked = uncertainty
                pred_stacked = prediction
            else:
                uncertainty_stacked = np.vstack((uncertainty_stacked, uncertainty))
                pred_stacked = np.vstack((pred_stacked, prediction))

        exp.uncertainty = uncertainty_stacked.T
        exp.prediction = pred_stacked.T

    @classmethod
    def fit_random_forest_with_jack_knife_variance_estimators(cls, exp):
        for i in range(len(self.targets)):
            if self.dataframe.loc[:, self.targets[i]].count() <= 1:
                raise ValueNotSupportedException(message=f'The given dataset does not contain enough training data '
                                                         f'in column {self.targets[i]}. Please ensure that there are '
                                                         f'at least 2 data points that are not filtered out by '
                                                         f'apriori thresholds.')

            # Initialize the model
            rfr = RandomForestRegressor()

            # Train the model
            training_rows = self.features_df.iloc[self.sample_index].to_numpy()
            training_labels = self.target_df.iloc[self.sample_index]

            self._check_target_label_validity(training_labels)

            self.x = training_rows
            self.y = training_labels.loc[:, self.targets[i]].to_frame().to_numpy()
            if self.y.shape[0] < 8:
                self.x = np.tile(self.x, (4, 1))
                self.y = np.tile(self.y, (4, 1))
            rfr.fit(self.x, self.y)

            # Predict the label for the remaining rows
            rows_to_predict = self.features_df.iloc[self.prediction_index]
            prediction, uncertainty = rfr.predict(rows_to_predict, return_std=True)

            if i == 0:
                uncertainty_stacked = uncertainty
                pred_stacked = prediction
            else:
                uncertainty_stacked = np.vstack((uncertainty_stacked, uncertainty))
                pred_stacked = np.vstack((pred_stacked, prediction))

        self.uncertainty = uncertainty_stacked.T
        self.prediction = pred_stacked.T

    def compute_novelty_factor(self):
        features_of_predicted_rows = self.features_df.iloc[self.prediction_index]
        features_of_known_rows = self.features_df.iloc[self.sample_index]

        distance = distance_matrix(features_of_predicted_rows, features_of_known_rows)
        min_distances = distance.min(axis=1)
        max_of_min_distances = min_distances.max()
        return min_distances * (max_of_min_distances ** (-1))

    def update_index_MLI(self):
        predicted_rows = self.target_df.loc[self.sample_index]
        # Normalize the uncertainty of the predicted labels
        uncertainty_norm = self.uncertainty / np.array(predicted_rows.std())

        clipped_prediction = self.clip_predictions()

        # Normalize the predicted labels
        prediction_norm = (clipped_prediction - np.array(predicted_rows.mean())) / np.array(predicted_rows.std())

        if self.prediction.ndim >= 2:
            # Scale the prediction and the uncertainty by the given weight for that target
            for w in range(len(self.target_weights)):
                prediction_norm[:, w] *= self.target_weights[w]
                uncertainty_norm[:, w] *= self.target_weights[w]
        else:
            # There is only one target property and weights do not matter
            # Nevertheless multiply by the single weight available
            prediction_norm *= self.target_weights[0]
            uncertainty_norm *= self.target_weights[0]

        self._normalize_data()

        if len(self.apriori_columns) > 0:
            apriori_values_for_predicted_rows = self.apply_weights_to_apriori_values()
        else:
            apriori_values_for_predicted_rows = np.zeros(len(self.prediction_index))

        # Compute the value of the utility function
        # See slide 43 of the PowerPoint presentation
        if len(self.targets) > 1:
            utility_function = apriori_values_for_predicted_rows.squeeze() + prediction_norm.sum(
                axis=1) + self.curiosity * uncertainty_norm.sum(axis=1)
        else:
            utility_function = apriori_values_for_predicted_rows.squeeze(
            ) + prediction_norm.squeeze() + self.curiosity * uncertainty_norm.squeeze()

        return utility_function

    def clip_predictions(self):
        if len(self.targets) == 1:
            if self.target_thresholds[0] is not None:
                if self.target_max_or_min[0] == 'min':
                    clipped_prediction = np.clip(self.prediction, a_min=self.target_thresholds[0], a_max=None)
                else:
                    clipped_prediction = np.clip(self.prediction, a_min=None, a_max=self.target_thresholds[0])
            else:
                clipped_prediction = self.prediction

        else:
            # Multiple targets
            column_indices = [i for i in range(len(self.targets))]
            clipped_predictions = []

            for (col_idx, value, threshold) in zip(column_indices, self.target_max_or_min, self.target_thresholds):
                if value not in ['min', 'max']:
                    raise SequentialLearningException(f'Invalid value for max_or_min, got {value}')
                if threshold is None:
                    clipped_predictions.append(self.prediction[:, col_idx])
                    continue

                if value == 'min':
                    clipped_predictions.append(np.clip(self.prediction[:, col_idx], a_min=threshold, a_max=None))
                elif value == 'max':
                    clipped_predictions.append(np.clip(self.prediction[:, col_idx], a_min=None, a_max=threshold))

            if clipped_predictions:
                clipped_prediction = np.vstack(clipped_predictions)
                clipped_prediction = clipped_prediction.T
            else:
                clipped_prediction = self.prediction

        return clipped_prediction



    @classmethod
    def _check_target_label_validity(cls, training_labels, exp):
        number_of_labelled_targets = training_labels.shape[0]
        if number_of_labelled_targets == 0:
            raise SequentialLearningException('No labels exist. Check your target and apriori columns and ensure '
                                              'your thresholds are set correctly.')

        # TODO: Check all_data_is_labelled in preprocessing
        all_data_is_labelled = exp.dataframe.shape[0] == number_of_labelled_targets
        if all_data_is_labelled:
            raise SequentialLearningException('All data is already labelled.')