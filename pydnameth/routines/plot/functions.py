import plotly.graph_objs as go
from pydnameth.config.experiment.types import DataType, Method
from pydnameth.routines.common import get_axis


def get_layout(config):

    if config.experiment.type == DataType.epimutations:

        if config.experiment.method == Method.scatter:

            y_title = 'SEM number'

            layout = go.Layout(
                title=dict(
                    font=dict(
                        family='Arial',
                        size=33,
                    )
                ),
                autosize=True,
                margin=go.layout.Margin(
                    l=120,
                    r=10,
                    b=80,
                    t=50,
                    pad=0
                ),
                barmode='overlay',
                legend=dict(
                    font=dict(
                        family='Arial',
                        size=16,
                    ),
                    orientation="h",
                    x=0.33,
                    y=1.11,
                ),
                xaxis=get_axis(config.attributes.target.capitalize()),
                yaxis=get_axis(y_title),
            )

            return layout
