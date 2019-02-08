from anytree import Node
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.config.experiment.types import DataType, Task, Method
from pydnameth.config.config import Config
from pydnameth.model.tree import calc_tree
from pydnameth.config.attributes.attributes import Attributes, Observables, Cells
import copy


def cpg_proc_table_linreg_dev(
    data,
    annotations,
    attributes,
    params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=Method.linreg,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes)
    )

    root = Node(name=str(config_root), config=config_root)
    calc_tree(root)


def cpg_proc_table_variance_linreg_dev(
    data,
    annotations,
    attributes,
    params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=Method.variance_linreg,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes)
    )

    root = Node(name=str(config_root), config=config_root)
    calc_tree(root)


def cpg_proc_table_polygon_dev(
    data,
    annotations,
    attributes,
    observables_list,
    child_method=Method.linreg,
    params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=Method.polygon,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes)
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
            experiment=Experiment(
                type=DataType.cpg,
                task=Task.table,
                method=copy.deepcopy(child_method),
                params={}
            ),
            annotations=copy.deepcopy(annotations),
            attributes=attributes_child
        )
        Node(name=str(config_child), config=config_child, parent=root)

    calc_tree(root)


def cpg_proc_table_z_test_linreg_dev(
    data,
    annotations,
    attributes,
    observables_list,
    child_method=Method.linreg,
    params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=Method.z_test_linreg,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes)
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
            experiment=Experiment(
                type=DataType.cpg,
                task=Task.table,
                method=copy.deepcopy(child_method),
                params={}
            ),
            annotations=copy.deepcopy(annotations),
            attributes=attributes_child
        )
        Node(name=str(config_child), config=config_child, parent=root)

    calc_tree(root)


def cpg_proc_clock_linreg_dev(
    data,
    annotations,
    attributes,
    child_method=Method.linreg,
    params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.clock,
            method=Method.linreg,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes)
    )
    root = Node(name=str(config_root), config=config_root)

    config_child = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=copy.deepcopy(child_method),
            params={}
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes)
    )

    Node(name=str(config_child), config=config_child, parent=root)

    calc_tree(root)


def cpg_plot_methylation_scatter_dev(
    data,
    annotations,
    attributes,
    cpg_list,
    observables_list,
    child_method=Method.linreg,
    params=None
):
    for cpg in cpg_list:

        config_root = Config(
            data=copy.deepcopy(data),
            experiment=Experiment(
                type=DataType.cpg,
                task=Task.methylation,
                method=Method.scatter,
                params=copy.deepcopy(params)
            ),
            annotations=copy.deepcopy(annotations),
            attributes=copy.deepcopy(attributes)
        )

        if config_root.experiment.params == None:
            config_root.experiment.params = dict()

        config_root.experiment.params['item'] = cpg

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
                experiment=Experiment(
                    type=DataType.cpg,
                    task=Task.table,
                    method=copy.deepcopy(child_method),
                    params={}
                ),
                annotations=copy.deepcopy(annotations),
                attributes=attributes_child,
                is_run=False
            )
            Node(name=str(config_child), config=config_child, parent=root)

        calc_tree(root)


def attributes_plot_observables_histogram_dev(
    data,
    annotations,
    attributes,
    observables_list,
    params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.attributes,
            task=Task.observables,
            method=Method.histogram,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes)
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
            is_run=False
        )
        Node(name=str(config_child), config=config_child, parent=root)

    calc_tree(root)
