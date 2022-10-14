from slamd.discovery.processing.experiment.plot_generator import PlotGenerator
from slamd.discovery.processing.models.tsne_plot_data import TSNEPlotData


class ExperimentPostprocessor:

    @classmethod
    def postprocess(cls, exp):
        # Construct dataframe for output

        df = exp.orig_data.loc[exp.index_predicted].copy()
        # Add the columns with utility and novelty values
        df['Utility'] = exp.utility.round(6)
        if exp.novelty is not None:
            df['Novelty'] = exp.novelty.round(6)

        for target in exp.target_names:
            df[target] = exp.prediction[target].round(6)
            df[f'Uncertainty ({target})'] = exp.uncertainty[target].round(5)

        df = cls.process_dataframe_for_output_table(df, exp)
        scatter_plot = cls.plot_output_space(df, exp)

        tsne_plot_data = TSNEPlotData(utility=exp.utility, features_df=exp.features_df,
                                      index_all_labelled=exp.index_all_labelled, index_none_labelled=exp.index_none_labelled)
        return df, scatter_plot, tsne_plot_data

    @classmethod
    def move_after_row_column(cls, df, cols_to_move=None):
        """
        Move one or several columns after the column named 'Row number'.
        """
        cols = df.columns.tolist()
        seg1 = cols[:list(cols).index('Row number') + 1]

        if cols_to_move is None:
            seg2 = []
        else:
            seg2 = cols_to_move

        # Make sure to remove overlapping elements between the segments
        seg1 = [i for i in seg1 if i not in seg2]
        seg3 = [i for i in cols if i not in seg1 + seg2]

        # Return a new dataset with the columns in the new order to be assigned to the same variable.
        return df[seg1 + seg2 + seg3]

    @classmethod
    def process_dataframe_for_output_table(cls, df, exp):
        """
        - Sort by Utility in decreasing order
        - Number the rows from 1 to n (length of the dataframe) to identify them easier on the plots.
        - Move Utility, Novelty, all the target columns and their uncertainties to the left of the dataframe.
        """
        df = df.sort_values(by='Utility', ascending=False)
        df.insert(loc=0, column='Row number', value=[i for i in range(1, len(df) + 1)])

        if exp.novelty is not None:
            cols_to_move = ['Utility', 'Novelty'] + exp.target_names
        else:
            cols_to_move = ['Utility'] + exp.target_names

        cols_to_move += [f'Uncertainty ({target})' for target in exp.target_names] + exp.apriori_names

        return cls.move_after_row_column(df, cols_to_move)

    @classmethod
    def plot_output_space(cls, df, exp):
        columns_for_plot = exp.target_names.copy()
        columns_for_plot.extend([f'Uncertainty ({target})' for target in exp.target_names])
        columns_for_plot.extend(['Utility', 'Row number'])

        if len(exp.apriori_names) > 0:
            columns_for_plot.extend(exp.apriori_names)

        return PlotGenerator.create_target_scatter_plot(df[columns_for_plot])
