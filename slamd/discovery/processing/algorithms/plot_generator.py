import json
import plotly
import plotly.express as px


class PlotGenerator:

    @classmethod
    def create_target_scatter_plot(cls, target_list):
        dimensions = [col for col in target_list.columns if col != 'Utility']
        fig = px.scatter_matrix(target_list, dimensions=dimensions, color='Utility',
                                title='Scatter matrix of target properties')
        fig.update_traces(diagonal_visible=False, showupperhalf=False)
        fig.update_layout(
            height=1000,
        )
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
