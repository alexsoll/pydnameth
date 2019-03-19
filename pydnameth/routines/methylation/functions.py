import plotly.graph_objs as go
from pydnameth.config.experiment.types import DataType


def get_layout(config):

    item = config.experiment.params['item']
    aux = config.cpg_gene_dict[item]
    if isinstance(aux, list):
        aux_str = ';'.join(aux)
    else:
        aux_str = str(aux)

    y_title = '$\\beta$'
    if config.experiment.type == DataType.residuals_common or config.experiment.type == DataType.residuals_special:
        y_title = 'residuals'

    layout = go.Layout(
        title=item + '(' + aux_str + ')',
        autosize=True,
        barmode='overlay',
        legend=dict(
            font=dict(
                family='sans-serif',
                size=16,
            ),
            orientation="h",
            x=0,
            y=1.15,
        ),
        xaxis=dict(
            title=config.attributes.target,
            showgrid=True,
            showline=True,
            mirror='ticks',
            titlefont=dict(
                family='Arial, sans-serif',
                size=24,
                color='black'
            ),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(
                family='Old Standard TT, serif',
                size=20,
                color='black'
            ),
            exponentformat='e',
            showexponent='all'
        ),
        yaxis=dict(
            title=y_title,
            showgrid=True,
            showline=True,
            mirror='ticks',
            titlefont=dict(
                family='Arial, sans-serif',
                size=24,
                color='black'
            ),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(
                family='Old Standard TT, serif',
                size=20,
                color='black'
            ),
            exponentformat='e',
            showexponent='all'
        ),

    )

    return layout
