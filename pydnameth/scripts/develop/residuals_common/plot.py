from pydnameth.config.experiment.types import Method, DataType
from pydnameth.scripts.develop.plot import plot_scatter


def residuals_common_plot_scatter(
    data,
    annotations,
    attributes,
    cpg_list,
    observables_list,
    child_method=Method.linreg,
    data_params=None,
    method_params=None
):
    plot_scatter(
        DataType.residuals_common,
        data,
        annotations,
        attributes,
        cpg_list,
        observables_list,
        child_method,
        data_params,
        method_params
    )
