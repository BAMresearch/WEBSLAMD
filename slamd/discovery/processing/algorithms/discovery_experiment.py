# Adapted from the original Sequential Learning App
# https://github.com/BAMresearch/SequentialLearningApp
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from lolopy.learners import RandomForestRegressor
from scipy.spatial import distance_matrix
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel


class DiscoveryExperiment():

    def __init__(
        self, dataframe, model, strategy, sigma, distance, targets, target_weights, target_max_or_min,
            fixed_targets, fixed_target_weights, fixed_target_max_or_min, features):
        self.dataframe = dataframe
        self.model = model
        self.strategy = strategy
        self.features_df = dataframe
        self.target_df = dataframe
        self.fixed_target_df = dataframe

        self.sigma = sigma
        self.distance = distance
        self.targets = targets
        self.target_weights = target_weights
        self.target_max_or_min = target_max_or_min
        self.fixed_targets = fixed_targets
        self.fixed_target_weights = fixed_target_weights
        self.fixed_target_max_or_min = fixed_target_max_or_min
        self.features = features

        first_selected_target = self.targets[0]
        self.PredIdx = pd.isnull(self.dataframe[[first_selected_target]]).to_numpy().nonzero()[0]
        self.SampIdx = self.dataframe.index.difference(self.PredIdx)

    def scale_data(self):

        dataframe_norm = (self.dataframe-self.dataframe.mean())/self.dataframe.std()
        target_df_norm = (self.target_df-self.target_df.mean())/self.target_df.std()
        features_df_norm = (self.features_df-self.features_df.mean())/self.features_df.std()
        fixed_target_df_norm = (self.fixed_target_df-self.fixed_target_df.mean())/self.fixed_target_df.std()

        self.features_df = features_df_norm
        self.target_df = target_df_norm
        self.dataframe = dataframe_norm
        self.fixed_target_df = fixed_target_df_norm

    # Utility Methods
    def decide_max_or_min(self, columns, max_or_min):
        for (column, value) in zip(columns, max_or_min):
            if (value == "minimize"):
                self.dataframe[column] = self.dataframe[column]*(-1)

    def start_learning(self):
        self.decide_max_or_min(self.targets, self.target_max_or_min)
        self.decide_max_or_min(self.fixed_targets, self.fixed_target_max_or_min)

        self.fixed_target_selection_idxs = self.fixed_targets

        self.fixed_target_df = self.dataframe[self.fixed_target_selection_idxs]

        self.target_selection_idxs = self.targets

        self.features_df = self.dataframe[self.features]
        self.target_df = self.dataframe[self.targets]

        self.decide_model(self.model)

        self.strategy = 'MLI (explore & exploit)'
        util = self.update_strategy(self.strategy)

        distance = distance_matrix(self.features_df.iloc[self.PredIdx], self.features_df.iloc[self.SampIdx])
        min_distances = distance.min(axis=1)
        max_of_min_distances = min_distances.max()

        novelty_factor = min_distances*(max_of_min_distances**(-1))

        # normierten datafram
        df = self.dataframe  # .abs
        df = df.iloc[self.PredIdx].assign(Utility=pd.Series(util).values)
        df = df.loc[self.PredIdx].assign(Novelty=pd.Series(novelty_factor).values)

        if self.Uncertainty.ndim > 1:
            for i in range(len(self.target_selection_idxs)):

                df[self.target_selection_idxs[i]] = self.Expected_Pred[:, i]
                uncertainty_name_column = 'Uncertainty ('+self.target_selection_idxs[i]+' )'
                df[uncertainty_name_column] = self.Uncertainty[:, i].tolist()

        else:
            df[self.target_selection_idxs] = self.Expected_Pred.reshape(len(self.Expected_Pred), 1)
            uncertainty_name_column = 'Uncertainty ('+self.target_selection_idxs+' )'
            df[uncertainty_name_column] = self.Uncertainty.reshape(len(self.Uncertainty), 1)

        show_df = df.sort_values(by='Utility', ascending=False)

        target_list = show_df[self.target_selection_idxs]
        if len(self.fixed_target_selection_idxs) > 0:
            target_list = pd.concat((target_list, show_df[self.fixed_target_selection_idxs]), axis=1)
        target_list = pd.concat((target_list, show_df['Utility']), axis=1)

        print('')
        print('Pareto plot (predicted property trade-off)')

        g = sns.PairGrid(target_list, diag_sharey=False, corner=True, hue="Utility")
        g.map_diag(sns.histplot, hue=None, color=".3")
        g.map_lower(sns.scatterplot)
        g.add_legend()
        plt.show()

        return show_df

    def weight_fixed_tars(self):

        fixed_targets_in_prediction = self.fixed_target_df.iloc[self.PredIdx].to_numpy()

        for weights in range(len(self.fixed_target_weights)):
            fixed_targets_in_prediction[weights] = fixed_targets_in_prediction[weights] * \
                self.fixed_target_weights[weights].value

        return fixed_targets_in_prediction.sum(axis=1)

    def updateIndexMLI(self):
        Uncertainty_norm = self.Uncertainty/np.array(self.target_df.iloc[self.SampIdx].std())
        Expected_Pred_norm = (
            self.Expected_Pred-np.array(self.target_df.iloc[self.SampIdx].mean()))/np.array(self.target_df.iloc[self.SampIdx].std())

        if(self.Expected_Pred.ndim >= 2):

            for weights in range(len(self.target_weights)):
                Expected_Pred_norm[:, weights] = Expected_Pred_norm[:, weights]*self.target_weights[weights].value
                Uncertainty_norm[:, weights] = Uncertainty_norm[:, weights]*self.target_weights[weights].value

        else:

            Expected_Pred_norm = Expected_Pred_norm*self.target_weights[0].value
            Uncertainty_norm = Uncertainty_norm*self.target_weights[0].value

        self.scale_data()

        if(len(self.fixed_targets) > 0):
            fixed_targets_in_prediction = self.weight_fixed_tars()
        else:
            fixed_targets_in_prediction = np.zeros(len(self.PredIdx))

        if(len(self.target_selection_idxs) > 1):
            util = fixed_targets_in_prediction.squeeze()+Expected_Pred_norm.sum(axis=1)+(self.sigma*Uncertainty_norm.sum(axis=1))
        else:
            util = fixed_targets_in_prediction.squeeze()+Expected_Pred_norm.squeeze()+(self.sigma*Uncertainty_norm.squeeze())

        return util

    def fit_GP(self):

        for i in range(len(self.target_selection_idxs)):

            kernel = ConstantKernel(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
            dtr = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)

            dtr.fit(self.features_df.iloc[self.SampIdx].to_numpy(),
                    self.target_df[self.target_selection_idxs[i]].iloc[self.SampIdx].to_numpy())
            pred, uncertainty = dtr.predict(self.features_df.iloc[self.PredIdx], return_std=True)

            if(i == 0):
                uncertainty_stacked = uncertainty
                pred_stacked = pred
            else:
                uncertainty_stacked = np.vstack((uncertainty_stacked, uncertainty))
                pred_stacked = np.vstack((pred_stacked, pred))

        self.Uncertainty = uncertainty_stacked.T
        self.Expected_Pred = pred_stacked.T

    def fit_RF_wJK(self):

        for i in range(len(self.target_selection_idxs)):

            dtr = RandomForestRegressor()
            self.x = self.features_df.iloc[self.SampIdx].to_numpy()
            self.y = self.target_df.iloc[self.SampIdx].sum(axis=1).to_frame().to_numpy()
            if self.y.shape[0] < 8:
                self.x = np.tile(self.x, (4, 1))
                self.y = np.tile(self.y, (4, 1))

            dtr.fit(self.x, self.y)
            pred, uncertainty = dtr.predict(self.features_df.iloc[self.PredIdx], return_std=True)

            if(i == 0):
                uncertainty_stacked = uncertainty
                pred_stacked = pred
            else:
                uncertainty_stacked = np.vstack((uncertainty_stacked, uncertainty))
                pred_stacked = np.vstack((pred_stacked, pred))

        self.Uncertainty = uncertainty_stacked.T
        self.Expected_Pred = pred_stacked.T

    def decide_model(self, model):
        if model == 'AI-Model (lolo Random Forrest)':
            self.fit_RF_wJK()
        elif model == 'Statistics based model (Gaussian Process Regression)':
            self.fit_GP()

    def update_strategy(self, strategy):
        if strategy == 'MEI (exploit)':
            util = self.updateIndexMEI()
        elif strategy == 'MU (explore)':
            util = self.updateIndexMU()
        elif strategy == 'MLI (explore & exploit)':
            util = self.updateIndexMLI()
        elif strategy == 'MEID (exploit)':
            util = self.updateIndexMEID()
        elif strategy == 'MLID (explore & exploit)':
            util = self.updateIndexMLID()
        return util
