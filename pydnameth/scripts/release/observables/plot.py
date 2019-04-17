from pydnameth.scripts.develop.observables.plot import observables_plot_histogram_dev


def observables_plot_histogram(
    data,
    annotations,
    attributes,
    observables_list,
    params=None
):
    """
    Plotting histogram for target observable distribution for provided subjects subsets and provided CpG list.

    Possible parameters of experiment:

    * ``'bin_size'``: bin size for numeric target. \n
      For categorical target is not considered.
    * ``'opacity'``: opacity level.
      From ``0.0`` to ``1.0``.
    * ``'barmode'``: type of barmode. \n
      Possible options: \n
      ``'overlay'`` for overlaid histograms. \n
      ``'stack'`` for stacked histograms. \n
    * ``'x_range'``: can be ``'auto'`` or list with two elements, which are borders of target axis.

    :param data: pdm.Data instance, which specifies information about dataset.
    :param annotations: pdm.Annotations instance, which specifies subset of CpGs.
    :param attributes: pdm.Attributes instance, which specifies information about subjects.
    :param cpg_list: List of CpGs for plotting
    :param observables_list: list of subjects subsets. Each element in list is dict,
     where ``key`` is observable name and ``value`` is possible values for this observable.
    :param params: parameters of experiment.
    """
    observables_plot_histogram_dev(
        data=data,
        annotations=annotations,
        attributes=attributes,
        observables_list=observables_list,
        params=params
    )
