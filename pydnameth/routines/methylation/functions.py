import plotly.graph_objs as go
from pydnameth.config.experiment.types import DataType
from pydnameth.routines.common import get_axis, get_legend, get_margin


def get_layout(config):

    item = config.experiment.params['item']
    if item in config.cpg_gene_dict:
        aux = config.cpg_gene_dict[item]
        if isinstance(aux, list):
            aux_str = ';'.join(aux)
        else:
            aux_str = str(aux)
    else:
        aux_str = 'non-genic'

    y_title = 'Methylation level'
    if config.experiment.type == DataType.residuals_common or config.experiment.type == DataType.residuals_special:
        y_title = 'residuals'

    layout = go.Layout(
        title=dict(
            text=item + '(' + aux_str + ')',
            font=dict(
                family='sans-serif',
                size=33,
            )
        ),
        autosize=True,
        margin=go.layout.Margin(
            l=95,
            r=10,
            b=80,
            t=85,
            pad=0
        ),
        barmode='overlay',
        legend=dict(
            font=dict(
                family='sans-serif',
                size=16,
            ),
            orientation="h",
            x=0.33,
            y=1.11,
        ),
        xaxis=get_axis(config.attributes.target),
        yaxis=get_axis(y_title),
    )

    return layout
