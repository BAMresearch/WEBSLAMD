import json

import numpy as np
import pandas as pd

from slamd.discovery.processing.experiment.plot_generator import PlotGenerator
from tests.discovery.processing.plotgenerator.scatter_1dim_json import SCATTER_1DIM_JSON
from tests.discovery.processing.plotgenerator.scatter_2dim_json import SCATTER_2DIM_JSON
from tests.discovery.processing.plotgenerator.tsne_3dim_json import TSNE_3DIM_JSON


def _plot_df_factory():
    plot_df = pd.DataFrame({
        't1': np.arange(20),
        't2': np.arange(0, 40, 2),
        't3': np.arange(20, 0, -1),
        'f1': np.arange(20),
        'f2': np.arange(0, 40, 2),
        'f3': np.arange(20, 0, -1),
    })

    plot_df['Uncertainty (t1)'] = plot_df['t1'] % 3 + 1
    plot_df['Uncertainty (t2)'] = (plot_df['t2'] % 3) * 2 + 2
    plot_df['Uncertainty (t3)'] = (plot_df['t3'] % 3) * 1.3 + 1.2

    plot_df['Utility'] = np.linspace(4, -2, 20)
    plot_df['Row number'] = plot_df.index
    plot_df['is_train_data'] = 'Predicted'
    plot_df.loc[15:, 'is_train_data'] = 'Labelled'

    # Reverse index to simulate an out-of-order index
    plot_df.index = plot_df.index[::-1]

    return plot_df


def test_create_target_scatter_plot_1dim():
    plot_df = _plot_df_factory().loc[:, ['t1', 'Uncertainty (t1)', 'Utility', 'Row number']]

    expected_output = SCATTER_1DIM_JSON
    actual_output = json.loads(PlotGenerator.create_target_scatter_plot(plot_df))

    assert expected_output == actual_output


def test_create_target_scatter_plot_2dim():
    plot_df = _plot_df_factory().loc[:, ['t1', 't2',  'Uncertainty (t1)', 'Uncertainty (t2)', 'Utility', 'Row number']]

    expected_output = SCATTER_2DIM_JSON
    actual_output = json.loads(PlotGenerator.create_target_scatter_plot(plot_df))

    assert expected_output == actual_output


def test_create_tsne_input_space_plot():
    plot_df = _plot_df_factory().loc[:, ['f1', 'f2', 'f3', 'Utility', 'Row number', 'is_train_data']]

    expected_output = TSNE_3DIM_JSON
    actual_output = json.loads(PlotGenerator.create_tsne_input_space_plot(plot_df))

    assert expected_output == actual_output
