import json
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
from itertools import combinations
from plotly.subplots import make_subplots
from sklearn.manifold import TSNE

UNCERTAINTY_COLUMN_PREFIX = 'Uncertainty ('


class PlotGenerator:

    @classmethod
    def create_target_scatter_plot(cls, plot_df):
        uncertainties = list(filter(lambda col: col.startswith(UNCERTAINTY_COLUMN_PREFIX), plot_df.columns))
        dimensions = list(filter(lambda col: col != 'Utility' and col !=
                          'Row number' and not col.startswith(UNCERTAINTY_COLUMN_PREFIX), plot_df.columns))

        if len(dimensions) == 1:
            # Generate a simple scatter plot if there is only one target property.
            # We include the Utility color-coded for aesthetic reasons.
            fig = px.scatter(
                plot_df,
                x=dimensions[0],
                y='Utility',
                color='Utility',
                custom_data=['Row number'],
                title='Scatter plot of target properties'
            )
            # Add light gray error bars and format tooltips rounding to two decimal places
            fig.update_traces(
                error_x=dict(
                    type='data',
                    array=cls._select_error_if_available(dimensions[0], uncertainties, plot_df),
                    color='lightgray',
                    thickness=1,
                ),
                hovertemplate='Row number: %{customdata}, X: %{x:.2f}, Y: %{y:.2f}, Utility: %{marker.color:.2f}'
            )
        else:
            # General case
            # For n target properties and a priori information columns, we need a (n-1) x (n-1) matrix
            matrix_size = len(dimensions) - 1
            fig = make_subplots(rows=matrix_size, cols=matrix_size, start_cell='top-left',
                                horizontal_spacing=0.01, vertical_spacing=0.01,
                                shared_xaxes=True, shared_yaxes=True)
            # Add title and remove the legend on the right that would show 'trace0', 'trace1', ...
            fig.update_layout(title='Scatter matrix of target properties', showlegend=False)

            # Generate possible indices for the lower-triangle of the (n-1) x (n-1) matrix
            row_indices, col_indices = np.tril_indices(n=matrix_size, k=0)
            # Increment all indices by one (numpy array operator overload)
            # because the first cell in the subplots is (1, 1)
            row_indices += 1
            col_indices += 1

            # Generate all possible combinations of ordered column names as tuples (x, y)
            axes = list(combinations(dimensions, 2))
            x_dimensions, y_dimensions = list(zip(*axes))
            for (x, y, row, col) in zip(x_dimensions, y_dimensions, row_indices, col_indices):
                scatter_plot = go.Scatter(
                    x=plot_df[x],
                    y=plot_df[y],
                    mode='markers',
                    marker=dict(
                        size=7,
                        color=plot_df['Utility'],
                        colorbar=dict(
                            title='Utility'
                        ),
                        colorscale='Plasma'
                    ),
                    customdata=plot_df['Row number'],
                    # Add light gray error bars for both dimensions
                    error_x=dict(
                        type='data',
                        array=cls._select_error_if_available(x, uncertainties, plot_df),
                        color='lightgray',
                        thickness=1,
                    ),
                    error_y=dict(
                        type='data',
                        array=cls._select_error_if_available(y, uncertainties, plot_df),
                        color='lightgray',
                        thickness=1,
                    ),
                    # Format tooltips for all cases rounding the displayed values to two decimal places.
                    hovertemplate='Row number: %{customdata}, X: %{x:.2f}, Y: %{y:.2f}, Utility: %{marker.color:.2f}',
                    # Make hover label have a black background
                    hoverlabel=dict(bgcolor='black'),
                    # Remove default name 'trace0', 'trace1', ...
                    name=''
                )
                if row == matrix_size:
                    # If on the bottom edge of the matrix
                    fig.update_xaxes(title_text=x, row=row, col=col)
                if col == 1:
                    # If on the left edge of the matrix
                    fig.update_yaxes(title_text=y, row=row, col=col)
                # Add subplot at given position
                fig.add_trace(scatter_plot, row=row, col=col)

        fig.update_layout(height=1000)
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @classmethod
    def create_tsne_input_space_plot(cls, plot_df):
        # The perplexity must be less than the number of data points (the length of the dataframe).
        # Handle this edge case by picking the smallest of the two.
        tsne = TSNE(n_components=2, verbose=1, perplexity=min(40, len(plot_df) - 1),
                    n_iter=300, random_state=1000, init='random', learning_rate=200)
        # Exclude the columns that do not belong to the features
        tsne_result = tsne.fit_transform(plot_df.drop(columns=['Row number', 'Utility', 'is_train_data']))
        tsne_result_df = pd.DataFrame(
            {'Row number': plot_df['Row number'],
             'tsne_1': tsne_result[:, 0],
             'tsne_2': tsne_result[:, 1],
             'Utility': plot_df['Utility'],
             'is_train_data': plot_df['is_train_data']}
        )
        fig = px.scatter(tsne_result_df, x='tsne_1', y='tsne_2', color='Utility', symbol='is_train_data',
                         custom_data=['Row number'],
                         title='Materials data in t-SNE coordinates: train data and targets',
                         symbol_sequence=['circle', 'cross'])
        fig.update_traces(
            hovertemplate='Row number: %{customdata}, Utility: %{marker.color:.2f}',
            marker=dict(size=7)
        )
        fig.update_layout(
            height=1000,
            legend_title_text="",
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @classmethod
    def _select_error_if_available(cls, column_name, uncertainties, df):
        error_column_name = f'{UNCERTAINTY_COLUMN_PREFIX}{column_name})'
        return df[error_column_name] if error_column_name in uncertainties else None
