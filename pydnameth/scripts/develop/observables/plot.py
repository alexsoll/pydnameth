import copy
from anytree import Node
from pydnameth.config.config import Config
from pydnameth.config.experiment.types import Task, Method, DataType
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.config.attributes.attributes import Observables, Cells, Attributes
from pydnameth.model.tree import build_tree, calc_tree


def observables_plot_histogram(
    data,
    annotations,
    attributes,
    observables_list,
    method_params=None
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
        :param method_params: parameters of experiment.
    """

    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=DataType.observables,
            task=Task.observables,
            method=Method.histogram,
            method_params=copy.deepcopy(method_params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True,
        is_load_child=False
    )
    root = Node(name=str(config_root), config=config_root)

    for d in observables_list:
        observables_child = Observables(
            name=copy.deepcopy(attributes.observables.name),
            types=d
        )

        cells_child = Cells(
            name=copy.deepcopy(attributes.cells.name),
            types=copy.deepcopy(attributes.cells.types)
        )

        attributes_child = Attributes(
            target=copy.deepcopy(attributes.target),
            observables=observables_child,
            cells=cells_child,
        )

        config_child = Config(
            data=copy.deepcopy(data),
            experiment=config_root.experiment,
            annotations=copy.deepcopy(annotations),
            attributes=attributes_child,
            is_run=False,
            is_root=True,
            is_load_child=False
        )
        Node(name=str(config_child), config=config_child, parent=root)

    build_tree(root)
    calc_tree(root)
