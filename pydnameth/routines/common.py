import plotly.graph_objs as go


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def normalize_to_0_1(values):
    values_normed = [(float(val) - min(values)) / (float(max(values)) - float(min(values))) for val in values]
    return values_normed


def get_axis(title):
    axis = dict(
        title=title,
        showgrid=True,
        showline=True,
        mirror='ticks',
        titlefont=dict(
            family='Arial',
            size=33,
            color='black'
        ),
        showticklabels=True,
        tickangle=0,
        tickfont=dict(
            family='Arial',
            size=30,
            color='black'
        ),
        exponentformat='e',
        showexponent='all'
    )
    return axis


def get_legend():
    legend = dict(
        font=dict(
            family='Arial',
            size=33,
        ),
        orientation="h",
        x=0.25,
        y=1.2,
    )
    return legend


def get_margin():
    margin = go.layout.Margin(
        l=80,
        r=20,
        b=80,
        t=10,
        pad=0
    )
    return margin


def get_names(config):
    name = str(config.attributes.observables)
    if 'gender' in name:
        name = name.replace('gender', 'sex')
    return name
