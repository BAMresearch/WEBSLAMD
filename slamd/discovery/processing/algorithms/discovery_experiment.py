# Adapted from the original Sequential Learning App
# https://github.com/BAMresearch/SequentialLearningApp
import numpy as np
import pandas as pd
from lolopy.learners import RandomForestRegressor
from scipy.spatial import distance_matrix
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel

from slamd.common.error_handling import ValueNotSupportedException, SequentialLearningException
from slamd.discovery.processing.algorithms.experiment_preprocessor import ExperimentPreprocessor
from slamd.discovery.processing.algorithms.plot_generator import PlotGenerator


# Attention - suppressing expected Gaussian Regressor warnings
import warnings
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)


class DiscoveryExperiment:

    @classmethod
    def run(cls, exp):
        ExperimentPreprocessor.preprocess(exp)

        cls.fit_model(exp)

        # The strategy is always 'MLI (explore & exploit)' for this implementation
        # See the original app for other possibilities
        utility_function = cls.update_index_MLI(exp)

        novelty_factor = cls.compute_novelty_factor(exp)

        # Construct dataframe for output
        df = exp.orig_data.loc[exp.nolabel_index].copy()
        # Add the columns with utility and novelty values
        df['Utility'] = utility_function.round(6)
        df['Novelty'] = novelty_factor.round(6)
        # df = df.iloc[self.prediction_index].assign(Utility=pd.Series(utility_function).values)
        # df = df.loc[self.prediction_index].assign(Novelty=pd.Series(novelty_factor).values)

        for target in exp.target_names:
            df[target] = exp.prediction[target].round(6)
            df[f'Uncertainty({target}'] = exp.uncertainty[target].round(5)

        df = cls.preprocess_dataframe_for_output_table(df, exp)
        scatter_plot = cls.plot_output_space(df, exp)
        tsne_plot = cls.plot_input_space(utility_function, exp)
        return df, scatter_plot, tsne_plot

    @classmethod
    def move_after_row_column(cls, df, cols_to_move=[]):
        """
        Move one or several columns after the column named 'Row number'.
        """
        cols = df.columns.tolist()
        seg1 = cols[:list(cols).index('Row number') + 1]
        seg2 = cols_to_move
        # Make sure to remove overlapping elements between the segments
        seg1 = [i for i in seg1 if i not in seg2]
        seg3 = [i for i in cols if i not in seg1 + seg2]
        # Return a new dataset with the columns in the new order to be assigned to the same variable.
        return df[seg1 + seg2 + seg3]

    @classmethod
    def preprocess_dataframe_for_output_table(cls, df, exp):
        """
        - Sort by Utility in decreasing order
        - Number the rows from 1 to n (length of the dataframe) to identify them easier on the plots.
        - Move Utility, Novelty, all the target columns and their uncertainties to the left of the dataframe.
        """
        df = df.sort_values(by='Utility', ascending=False)
        df.insert(loc=0, column='Row number', value=[i for i in range(1, len(df) + 1)])
        cols_to_move = ['Utility', 'Novelty'] + exp.target_names
        cols_to_move += [f'Uncertainty ({target})' for target in exp.target_names] +\
                        exp.apriori_names
        return cls.move_after_row_column(df, cols_to_move)

    @classmethod
    def plot_output_space(cls, df, exp):
        columns_for_plot = exp.target_names.copy()
        columns_for_plot.extend(['Utility', 'Row number'])
        if len(exp.apriori_names) > 0:
            columns_for_plot.extend(exp.apriori_names)
        return PlotGenerator.create_target_scatter_plot(df[columns_for_plot])

    @classmethod
    def plot_input_space(cls, utility_function, exp):
        plot_df = exp.features_df.copy()
        plot_df['is_train_data'] = 'Predicted'
        plot_df['is_train_data'].iloc[exp.label_index] = 'Labelled'
        plot_df['Utility'] = -np.inf
        plot_df['Utility'].iloc[exp.nolabel_index] = pd.Series(utility_function).values
        plot_df = plot_df.sort_values(by='Utility', ascending=False)
        # Number the rows from 1 to n (length of the dataframe) to identify them easier on the plots.
        plot_df.insert(loc=0, column='Row number', value=[i for i in range(1, len(plot_df) + 1)])
        return PlotGenerator.create_tsne_input_space_plot(plot_df)


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
            training_labels = exp.targets_df.loc[exp.label_index, target].values

            gpr.fit(training_rows, training_labels)

            # Predict the label for the remaining rows
            rows_to_predict = exp.features_df.loc[exp.nolabel_index].values
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
            training_labels = exp.targets_df.loc[exp.label_index, target].values

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
        # TODO predicted_rows is misleadingly named! not actually predicted!
        predicted_rows = exp.targets_df.loc[exp.label_index].copy()

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
        if len(exp.target_names) > 1:
            utility = apriori_values_for_predicted_rows.squeeze() + normed_prediction.sum(axis=1) +\
                               exp.curiosity * normed_uncertainty.sum(axis=1)
        else:
            utility = apriori_values_for_predicted_rows.squeeze() + normed_prediction.squeeze() +\
                               exp.curiosity * normed_uncertainty.squeeze()

        # TODO This can probably be written into a dataframe
        return utility

    @classmethod
    def compute_novelty_factor(cls, exp):
        features_of_predicted_rows = exp.features_df.iloc[exp.nolabel_index]
        features_of_known_rows = exp.features_df.iloc[exp.label_index]

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

    @classmethod
    def apply_weights_to_apriori_values(cls, exp):
        apriori_for_predicted_rows = exp.apriori_df.loc[exp.nolabel_index]

        for (col, weight) in zip(exp.apriori_df.columns, exp.apriori_weights):
            apriori_for_predicted_rows[col] *= weight

        # Sum the apriori values row-wise for the case that there are several of them
        # We need to simply add their contributions in that case
        return apriori_for_predicted_rows.sum(axis=1)
