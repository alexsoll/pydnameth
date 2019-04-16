from pydnameth.config.experiment.types import Method
from pydnameth.scripts.develop.betas.plot import betas_plot_scatter_dev


def cpg_plot_methylation_scatter(
    data,
    annotations,
    attributes,
    cpg_list,
    observables_list,
    params=None
):
    """
    Plotting methylation level from observables as scatter for provided subjects subsets and provided CpG list.

    Possible parameters of experiment:

     * ``'x_range'``: can be ``'auto'`` or list with two elements, which are borders of target axis.
     * ``'details'``: what to plot?.
     Possible options: \n
      ``0``: display only methylation levels points. \n
      ``1``: display levels: ``0``. Also display linear regression line. \n
      ``2``: display levels: ``0``, ``1``. Also display polygon. \n

    :param data: pdm.Data instance, which specifies information about dataset.
    :param annotations: pdm.Annotations instance, which specifies subset of CpGs.
    :param attributes: pdm.Attributes instance, which specifies information about subjects.
    :param cpg_list: List of CpGs for plotting
    :param observables_list: list of subjects subsets. Each element in list is dict,
     where ``key`` is observable name and ``value`` is possible values for this observable.
    :param params: parameters of experiment.
    """

    child_method = Method.linreg

    betas_plot_scatter_dev(
        data=data,
        annotations=annotations,
        attributes=attributes,
        cpg_list=cpg_list,
        observables_list=observables_list,
        child_method=child_method,
        method_params=params
    )
