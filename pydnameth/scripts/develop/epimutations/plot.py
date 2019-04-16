import copy
from anytree import Node
from pydnameth.config.config import Config
from pydnameth.config.experiment.types import Task, Method, DataType
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.config.attributes.attributes import Observables, Cells, Attributes
from pydnameth.model.tree import build_tree, calc_tree


def epimutations_plot_scatter_dev(
    data,
    annotations,
    attributes,
    observables_list,
    method_params=None
):
    epimutations_plot(
        data,
        annotations,
        attributes,
        observables_list,
        Method.scatter,
        method_params
    )


def epimutations_plot_range_dev(
    data,
    annotations,
    attributes,
    observables_list,
    method_params=None
):
    epimutations_plot(
        data,
        annotations,
        attributes,
        observables_list,
        Method.range,
        method_params
    )


def epimutations_plot(
    data,
    annotations,
    attributes,
    observables_list,
    method,
    method_params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=DataType.epimutations,
            task=Task.plot,
            method=method,
            method_params=copy.deepcopy(method_params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
    )

    root = Node(name=str(config_root), config=config_root)

    for types in observables_list:
        observables_child = Observables(
            name=copy.deepcopy(attributes.observables.name),
            types=types
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
            experiment=Experiment(
                data=DataType.epimutations,
                task=Task.table,
                method=Method.mock
            ),
            annotations=copy.deepcopy(annotations),
            attributes=attributes_child,
            is_run=False,
            is_root=False
        )
        Node(name=str(config_child), config=config_child, parent=root)

    build_tree(root)
    calc_tree(root)
