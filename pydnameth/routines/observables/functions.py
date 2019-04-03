import plotly.graph_objs as go


def get_names(config):
    name = str(config.attributes.observables)
    if 'gender' in name:
        name = name.replace('gender', 'sex')
    return name


def get_layout(config):

    layout = go.Layout(
        autosize=True,
        margin=go.layout.Margin(
            l=80,
            r=20,
            b=80,
            t=10,
            pad=0
        ),
        barmode=config.experiment.params['barmode'],
        legend=dict(
            font=dict(
                family='sans-serif',
                size=33,
            ),
            orientation="h",
            x=0.25,
            y=1.2,
        ),
        xaxis=dict(
            title=config.attributes.target,
            showgrid=True,
            showline=True,
            mirror='ticks',
            titlefont=dict(
                family='Arial, sans-serif',
                size=33,
                color='black'
            ),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(
                family='Old Standard TT, serif',
                size=30,
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
                size=33,
                color='black'
            ),
            showticklabels=True,
            tickangle=0,
            tickfont=dict(
                family='Old Standard TT, serif',
                size=30,
                color='black'
            ),
            exponentformat='e',
            showexponent='all'
        ),

    )

    return layout
