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

        # The strategy is always 'MLI (explore & exploit)' for this implementation
        # See the original app for other possibilities
        utility_function = cls.update_index_MLI(exp)

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
        # TODO I am 99% sure you can fit the same gpr object multiple times, verify
        # Initialize the model with given hyperparameters
        kernel = ConstantKernel(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
        gpr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9, random_state=42)

        predictions = {}
        uncertainties = {}
        for target in exp.target_names:
            # Train the GPR model for every target with the corresponding rows and labels
            training_rows = exp.features_df.loc[exp.label_index].values
            training_labels = exp.targets_df.loc[exp.nolabel_index, target].values

            gpr.fit(training_rows, training_labels)

            # Predict the label for the remaining rows
            rows_to_predict = exp.features_df.loc[exp.nolabel_index]
            prediction, uncertainty = gpr.predict(rows_to_predict, return_std=True)

            predictions[target] = prediction
            uncertainties[target] = uncertainty

        exp.prediction = pd.DataFrame(predictions)
        exp.uncertainty = pd.DataFrame(uncertainties)

    @classmethod
    def fit_random_forest_with_jack_knife_variance_estimators(cls, exp):
        # TODO This is very similar to fit_gaussian. Could feasibly be turned into a single function
        rfr = RandomForestRegressor()

        predictions = {}
        uncertainties = {}
        for target in exp.target_names:
            # Train the model
            training_rows = exp.features_df.loc[exp.label_index].values
            training_labels = exp.targets_df.loc[exp.nolabel_index, target].values

            # Artificially pad data to work with lolopy random forest implementation, if necessary
            if training_labels.shape[0] < 8:
                training_rows = np.tile(training_rows, (4, 1))
                training_labels = np.tile(training_labels, (4, 1))

            rfr.fit(training_rows, training_labels)

            # Predict the label for the remaining rows
            rows_to_predict = exp.features_df.loc[exp.nolabel_index]
            prediction, uncertainty = rfr.predict(rows_to_predict, return_std=True)

            predictions[target] = prediction
            uncertainties[target] = uncertainty

        exp.prediction = pd.DataFrame(predictions)
        exp.uncertainty = pd.DataFrame(uncertainties)

    @classmethod
    def update_index_MLI(cls, exp):
        # TODO rename to "predicted_results" or "predicted_labels"
        predicted_rows = exp.targets_df.loc[exp.nolabel_index].copy()

        # Normalize the uncertainty of the predicted labels, then clip to given thresholds
        # TODO What if the standard deviation is 0? also further down
        normed_uncertainty = exp.uncertainty / predicted_rows.std()
        clipped_prediction = cls.clip_prediction(exp)

        # Normalize the predicted labels
        normed_prediction = (clipped_prediction - predicted_rows.mean()) / predicted_rows.std()

        for (target, weight) in zip(exp.target_names, exp.target_weights):
            normed_prediction[target] *= weight
            normed_uncertainty[target] *= weight

        cls._normalize_data(exp)

        if len(exp.apriori_names) > 0:
            apriori_values_for_predicted_rows = cls.apply_weights_to_apriori_values(exp)
        else:
            apriori_values_for_predicted_rows = np.zeros(len(exp.nolabel_index)) # TODO which index?

        # Compute the value of the utility function
        # See slide 43 of the PowerPoint presentation
        # TODO This can probably be turned into a single expression
        if len(exp.targets) > 1:
            utility = apriori_values_for_predicted_rows.squeeze() + normed_prediction.sum(axis=1) +\
                               exp.curiosity * normed_uncertainty.sum(axis=1)
        else:
            utility = apriori_values_for_predicted_rows.squeeze() + normed_prediction.squeeze() +\
                               exp.curiosity * normed_uncertainty.squeeze()

        # TODO This can probably be written into a dataframe
        return utility

    def compute_novelty_factor(self):
        features_of_predicted_rows = self.features_df.iloc[self.prediction_index]
        features_of_known_rows = self.features_df.iloc[self.sample_index]

        distance = distance_matrix(features_of_predicted_rows, features_of_known_rows)
        min_distances = distance.min(axis=1)
        max_of_min_distances = min_distances.max()
        return min_distances * (max_of_min_distances ** (-1))

    @classmethod
    def clip_prediction(cls, exp):
        clipped_prediction = exp.prediction.copy()
        for (target, max_or_min, threshold) in zip(exp.target_names, exp.target_max_or_min, exp.target_thresholds):
            if max_or_min not in ['min', 'max']:
                raise SequentialLearningException(f'Invalid value for max_or_min, got {max_or_min}')

            if threshold is None:
                continue

            if max_or_min == 'min':
                clipped_prediction[target].clip(lower=threshold)
            elif max_or_min == 'max':
                clipped_prediction[target].clip(upper=threshold)

        return clipped_prediction

    @classmethod
    def _normalize_data(cls, exp):
        # TODO What about categoricals?
        # TODO What happens to the data afterwards? This is a destructive operation
        # replace 0s with 1s for division
        std = exp.dataframe.std().replace(0, 1)
        exp.dataframe = (exp.dataframe - exp.dataframe.mean()) / std

    def apply_weights_to_apriori_values(self):
        apriori_for_predicted_rows = self.apriori_df.iloc[self.prediction_index].to_numpy()

        for w in range(len(self.apriori_weights)):
            apriori_for_predicted_rows[w] *= self.apriori_weights[w]
        # Sum the apriori values row-wise for the case that there are several of them
        # We need to simply add their contributions in that case
        return apriori_for_predicted_rows.sum(axis=1)