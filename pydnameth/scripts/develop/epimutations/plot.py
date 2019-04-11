import copy
from anytree import Node
from pydnameth import Config, Experiment, DataType, Task, Method, Observables, Cells, Attributes
from pydnameth.model.tree import build_tree, calc_tree


def epimutations_plot_scatter_dev(
    data,
    annotations,
    attributes,
    observables_list,
    params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.epimutations,
            task=Task.plot,
            method=Method.scatter,
            params=copy.deepcopy(params)
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
                type=DataType.epimutations,
                task=Task.table,
                method=Method.mock,
                params={}
            ),
            annotations=copy.deepcopy(annotations),
            attributes=attributes_child,
            is_run=False,
            is_root=False
        )
        Node(name=str(config_child), config=config_child, parent=root)

    build_tree(root)
    calc_tree(root)
