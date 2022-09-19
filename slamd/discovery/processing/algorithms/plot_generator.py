import json
import plotly
import plotly.express as px


class PlotGenerator:

    @classmethod
    def create_target_scatter_plot(cls, target_list):
        dimensions = [col for col in target_list.columns if col != 'Utility']
        if len(dimensions) == 1:
            # Generate a simple scatter plot if there is only one target property
            fig = px.scatter(target_list, x=dimensions[0], y='Utility')
            fig.update_traces(hovertemplate='X: %{x:.2f}, Y: %{y:.2f}')
        elif len(dimensions) == 2:
            # Plotly 5.10 issue: px.scatter_matrix() does not output anything when the matrix is 1x1.
            # We need to handle this case separately and generate a single scatter plot.
            fig = px.scatter(target_list, x=dimensions[0], y=dimensions[1],
                             color='Utility', title='Scatter plot of target properties')
            fig.update_traces(hovertemplate='X: %{x:.2f}, Y: %{y:.2f}, Utility: %{marker.color:.2f}')
        else:
            # General case
            fig = px.scatter_matrix(target_list, dimensions=dimensions, color='Utility',
                                    title='Scatter matrix of target properties')
            # Format the tooltips in a generic way good enough for all subplots
            fig.update_traces(diagonal_visible=False, showupperhalf=False,
                              hovertemplate='X: %{x:.2f}, Y: %{y:.2f}, Utility: %{marker.color:.2f}')

        fig.update_layout(height=1000)
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
