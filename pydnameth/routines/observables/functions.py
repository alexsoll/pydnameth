import plotly.graph_objs as go
from pydnameth.routines.common import get_axis, get_legend, get_margin


def get_layout(config):

    layout = go.Layout(
        autosize=True,
        margin=get_margin(),
        barmode=config.experiment.params['barmode'],
        legend=get_legend(),
        xaxis=get_axis(config.attributes.target.capitalize()),
        yaxis=get_axis('Count'),
    )

    return layout
