import json
import pandas as pd
import plotly
import plotly.express as px
from sklearn.manifold import TSNE


class PlotGenerator:

    @classmethod
    def create_target_scatter_plot(cls, plot_df):
        dimensions = [col for col in plot_df.columns if col != 'Utility' and col != 'Row number']
        if len(dimensions) == 1:
            # Generate a simple scatter plot if there is only one target property.
            # We include the Utility color-coded for aesthetic reasons.
            fig = px.scatter(plot_df, x=dimensions[0], y='Utility', color='Utility',
                             custom_data=['Row number'], title='Scatter plot of target properties')
        elif len(dimensions) == 2:
            # Plotly 5.10 issue: px.scatter_matrix() does not output anything when the matrix is 1x1.
            # We need to handle this case separately and generate a single scatter plot.
            fig = px.scatter(plot_df, x=dimensions[0], y=dimensions[1], color='Utility',
                             custom_data=['Row number'], title='Scatter plot of target properties')
        else:
            # General case
            fig = px.scatter_matrix(plot_df, dimensions=dimensions, color='Utility',
                                    custom_data=['Row number'], title='Scatter matrix of target properties')
            fig.update_traces(diagonal_visible=False, showupperhalf=False)

        # Format tooltips for all cases rounding the displayed values to two decimal places.
        fig.update_traces(
            hovertemplate='Row number: %{customdata}, X: %{x:.2f}, Y: %{y:.2f}, Utility: %{marker.color:.2f}'
        )
        fig.update_layout(height=1000)
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @classmethod
    def create_tsne_input_space_plot(cls, features_df, candidate_or_target):
        tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300, random_state=1000,
                    init='random', learning_rate=200)
        tsne_result = tsne.fit_transform(features_df)
        tsne_result_df = pd.DataFrame(
            {'tsne_1': tsne_result[:, 0],
             'tsne_2': tsne_result[:, 1],
             'candidate_or_target': candidate_or_target}
        )

        fig = px.scatter(tsne_result_df, x='tsne_1', y='tsne_2', color='candidate_or_target',
                         title='Materials data in t-SNE coordinates: candidates and targets')
        fig.update_traces(
            hovertemplate='X: %{x:.2f}, Y: %{y:.2f}'
        )
        fig.update_layout(height=1000)
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
