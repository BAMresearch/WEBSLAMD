import numpy as np
import pandas as pd

from slamd.discovery.processing.algorithms.plot_generator import PlotGenerator


class ExperimentPostprocessor:
    @classmethod
    def postprocess(cls, exp, utility, novelty):

        # Construct dataframe for output
        df = exp.orig_data.loc[exp.nolabel_index].copy()
        # Add the columns with utility and novelty values
        df['Utility'] = utility
        df['Utility'] = df['Utility'].round(6)
        df['Novelty'] = novelty.round(6)
        # df = df.iloc[self.prediction_index].assign(Utility=pd.Series(utility_function).values)
        # df = df.loc[self.prediction_index].assign(Novelty=pd.Series(novelty_factor).values)

        # TODO prediction index mismatch
        for target in exp.target_names:
            df.loc[exp.nolabel_index, target] = exp.prediction[target].values
            df[target] = df[target].round(6)
            df[f'Uncertainty ({target})'] = exp.uncertainty[target].values
            df[f'Uncertainty ({target})'] = df[f'Uncertainty ({target})'].round(5)

        df = cls.preprocess_dataframe_for_output_table(df, exp)
        scatter_plot = cls.plot_output_space(df, exp)
        tsne_plot = cls.plot_input_space(utility, exp)
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
        cols_to_move += [f'Uncertainty ({target})' for target in exp.target_names] + \
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










