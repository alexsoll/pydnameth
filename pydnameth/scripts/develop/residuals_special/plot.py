from pydnameth.config.experiment.types import Method, DataType
from pydnameth.scripts.develop.plot import plot_scatter


def residuals_special_plot_scatter(
    data,
    annotations,
    attributes,
    cpg_list,
    observables_list,
    child_method=Method.linreg,
    params=None
):
    plot_scatter(
        DataType.residuals_special,
        data,
        annotations,
        attributes,
        cpg_list,
        observables_list,
        child_method,
        params
    )
