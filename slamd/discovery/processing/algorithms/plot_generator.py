import json
import base64
from io import BytesIO

from matplotlib import pyplot as plt
import plotly
import plotly.express as px
import seaborn as sns


class PlotGenerator:

    @classmethod
    def create_target_scatter_plot(cls, target_list):
        static_plot = cls._create_static_plot(target_list)
        interactive_plot = cls._create_interactive_plot(target_list)
        return static_plot, interactive_plot

    @classmethod
    def _create_static_plot(cls, target_list):
        grid = sns.PairGrid(target_list, diag_sharey=False, corner=True, hue='Utility')
        grid.map_diag(sns.histplot, hue=None, color='.3')
        grid.map_lower(sns.scatterplot)
        grid.add_legend()
        plt.plot()
        img_bytes = BytesIO()
        plt.savefig(img_bytes, format='png')
        plt.close()
        img_bytes.seek(0)
        return base64.b64encode(img_bytes.getvalue()).decode()

    @classmethod
    def _create_interactive_plot(cls, target_list):
        dimensions = [col for col in target_list.columns if col != 'Utility']
        fig = px.scatter_matrix(target_list, dimensions=dimensions, color='Utility',
                                title='Scatter matrix of target properties')
        fig.update_traces(diagonal_visible=False, showupperhalf=False)
        fig.update_layout(
            height=1000,
        )
        return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
