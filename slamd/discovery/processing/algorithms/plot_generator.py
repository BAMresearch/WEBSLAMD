import base64
from io import BytesIO

from matplotlib import pyplot as plt
import seaborn as sns


class PlotGenerator:

    @classmethod
    def create_target_scatter_plot(cls, target_list):
        img = BytesIO()

        grid = sns.PairGrid(target_list, diag_sharey=False, corner=True, hue="Utility")
        grid.map_diag(sns.histplot, hue=None, color=".3")
        grid.map_lower(sns.scatterplot)
        grid.add_legend()
        plt.plot()
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)

        return base64.b64encode(img.getvalue()).decode()
