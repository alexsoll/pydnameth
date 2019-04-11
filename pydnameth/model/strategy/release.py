import abc
import numpy as np
from pydnameth.config.experiment.types import DataType, Method
from pydnameth.config.experiment.types import get_main_metric
import plotly.graph_objs as go
from statsmodels.stats.multitest import multipletests
import plotly.figure_factory as ff
import pydnameth.routines.plot.functions as plot_routines
import pydnameth.routines.methylation.functions as methylation_routines
import pydnameth.routines.observables.functions as observables_routines


class ReleaseStrategy(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def release(self, config, configs_child):
        pass


class TableReleaseStrategy(ReleaseStrategy):

    def release(self, config, configs_child):
        if config.experiment.method == Method.z_test_linreg:
            reject, pvals_corr, alphacSidak, alphacBonf = multipletests(config.metrics['p_value'],
                                                                        0.05,
                                                                        method='fdr_bh')
            config.metrics['p_value'] = pvals_corr

        (key, direction) = get_main_metric(config.experiment)

        order = list(np.argsort(config.metrics[key]))
        if direction == 'descending':
            order.reverse()

        for key, value in config.metrics.items():
            config.metrics[key] = list(np.array(value)[order])


class ClockReleaseStrategy(ReleaseStrategy):

    def release(self, config, configs_child):
        pass


class MethylationReleaseStrategy(ReleaseStrategy):

    def release(self, config, configs_child):

        if config.experiment.method == Method.scatter:

            layout = methylation_routines.get_layout(config)

            if 'x_range' in config.experiment.params:
                if config.experiment.params['x_range'] != 'auto':
                    layout.xaxis.range = config.experiment.params['x_range']

            if 'y_range' in config.experiment.params:
                if config.experiment.params['y_range'] != 'auto':
                    layout.yaxis.range = config.experiment.params['y_range']

            config.experiment_data['fig'] = go.Figure(data=config.experiment_data['data'], layout=layout)

        elif config.experiment.method == Method.variance_histogram:

            layout = methylation_routines.get_layout(config)
            layout.xaxis.title = '$\\Delta$'
            layout.yaxis.title = '$PDF$'

            fig = ff.create_distplot(
                config.experiment_data['data']['hist_data'],
                config.experiment_data['data']['group_labels'],
                show_hist=False,
                show_rug=False,
                colors=config.experiment_data['data']['colors']
            )
            fig['layout'] = layout

            config.experiment_data['fig'] = fig


class PlotReleaseStrategy(ReleaseStrategy):

    def release(self, config, configs_child):

        if config.experiment.type == DataType.epimutations:

            if config.experiment.method == Method.scatter:

                layout = plot_routines.get_layout(config)

                if config.experiment.params['x_range'] != 'auto':
                    layout.xaxis.range = config.experiment.params['x_range']

                if config.experiment.params['y_range'] != 'auto':
                    layout.yaxis.range = config.experiment.params['y_range']

                layout.yaxis.type = config.experiment.params['y_type']
                if layout.yaxis.type == 'log':
                    layout.yaxis.tickvals = [1, 2, 5,
                                             10, 20, 50,
                                             100, 200, 500,
                                             1000, 2000, 5000,
                                             10000, 20000, 50000,
                                             100000, 200000, 500000]

                config.experiment_data['fig'] = go.Figure(data=config.experiment_data['data'], layout=layout)


class ObservablesReleaseStrategy(ReleaseStrategy):

    def release(self, config, configs_child):

        if config.experiment.method == Method.histogram:

            layout = observables_routines.get_layout(config)

            if 'x_range' in config.experiment.params:
                if config.experiment.params['x_range'] != 'auto':
                    layout.xaxis.range = config.experiment.params['x_range']

            config.experiment_data['fig'] = go.Figure(data=config.experiment_data['data'], layout=layout)
