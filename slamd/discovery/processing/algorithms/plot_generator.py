import base64
from io import BytesIO

from matplotlib import pyplot as plt
import seaborn as sns


class PlotGenerator:

    @classmethod
    def create_target_scatter_plot(cls, target_list):
        grid = sns.PairGrid(target_list, diag_sharey=False, corner=True, hue="Utility")
        grid.map_diag(sns.histplot, hue=None, color=".3")
        grid.map_lower(sns.scatterplot)
        grid.add_legend()
        plt.plot()

        img_bytes = BytesIO()
        plt.savefig(img_bytes, format='png')
        plt.close()
        img_bytes.seek(0)

        return base64.b64encode(img_bytes.getvalue()).decode()
