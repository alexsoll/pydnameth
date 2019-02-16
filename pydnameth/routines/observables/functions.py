import plotly.graph_objs as go


def get_layout(config):

    layout = go.Layout(
        autosize=True,
        barmode=config.experiment.params['barmode'],
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
            title='count',
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
