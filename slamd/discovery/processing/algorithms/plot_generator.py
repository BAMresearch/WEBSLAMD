import json
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
            # Format the tooltips in a generic way good enough for all subplots
            fig.update_traces(diagonal_visible=False, showupperhalf=False)

        fig.update_traces(
            hovertemplate='Row number: %{customdata}, X: %{x:.2f}, Y: %{y:.2f}, Utility: %{marker.color:.2f}'
        )
        fig.update_layout(height=1000)
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    @classmethod
    def create_tsne_input_space_plot(cls, features_df):
        tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300, random_state=1000)
        features_df_embedded = tsne.fit_transform(features_df)
        x_embedded = [x for (x, _) in features_df_embedded]
        y_embedded = [y for (_, y) in features_df_embedded]

        fig = px.scatter(x=x_embedded, y=y_embedded,
                         title='Materials data in t-SNE coordinates: candidates and targets')

        fig.update_layout(height=1000)
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
