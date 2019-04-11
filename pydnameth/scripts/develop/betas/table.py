import copy
from anytree import Node
from pydnameth.config.config import Config
from pydnameth.config.experiment.types import Task, Method, DataType
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.config.attributes.attributes import Observables, Cells, Attributes
from pydnameth.model.tree import build_tree, calc_tree
from pydnameth.scripts.develop.table import table_linreg, table_aggregator


def betas_table_linreg_dev(
    data,
    annotations,
    attributes,
    params=None
):
    table_linreg(
        DataType.betas,
        data,
        annotations,
        attributes,
        params
    )


def betas_table_variance_linreg_dev(
    data,
    annotations,
    attributes,
    params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.betas,
            task=Task.table,
            method=Method.variance_linreg,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
    )

    root = Node(name=str(config_root), config=config_root)
    build_tree(root)
    calc_tree(root)


def betas_table_polygon_dev(
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
            type=DataType.betas,
            task=Task.table,
            method=Method.polygon,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
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
                type=DataType.betas,
                task=Task.table,
                method=copy.deepcopy(child_method),
                params={}
            ),
            annotations=copy.deepcopy(annotations),
            attributes=attributes_child,
            is_run=True,
            is_root=False
        )
        Node(name=str(config_child), config=config_child, parent=root)

    build_tree(root)
    calc_tree(root)


def betas_table_z_test_linreg_dev(
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
            type=DataType.betas,
            task=Task.table,
            method=Method.z_test_linreg,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
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
                type=DataType.betas,
                task=Task.table,
                method=copy.deepcopy(child_method),
                params={}
            ),
            annotations=copy.deepcopy(annotations),
            attributes=attributes_child,
            is_run=True,
            is_root=False
        )
        Node(name=str(config_child), config=config_child, parent=root)

    build_tree(root)
    calc_tree(root)


def betas_table_aggregator_dev(
    data,
    annotations,
    attributes,
    observables_list,
    params=None
):
    table_aggregator(
        DataType.betas,
        data,
        annotations,
        attributes,
        observables_list,
        params
    )


def betas_table_aggregator_var_dev(
    data,
    annotations,
    attributes,
    observables_list,
    params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.betas,
            task=Task.table,
            method=Method.aggregator,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
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
                type=DataType.betas,
                task=Task.table,
                method=copy.deepcopy(Method.variance_linreg),
                params={}
            ),
            annotations=copy.deepcopy(annotations),
            attributes=attributes_child,
            is_run=True,
            is_root=False
        )
        Node(name=str(config_child), config=config_child, parent=root)

    observables_cluster = Observables(
        name=copy.deepcopy(attributes.observables.name),
        types={}
    )

    cells_cluster = Cells(
        name=copy.deepcopy(attributes.cells.name),
        types=copy.deepcopy(attributes.cells.types)
    )

    attributes_cluster = Attributes(
        target=copy.deepcopy(attributes.target),
        observables=observables_cluster,
        cells=cells_cluster,
    )

    config_cluster = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.betas,
            task=Task.table,
            method=copy.deepcopy(Method.cluster),
            params={}
        ),
        annotations=copy.deepcopy(annotations),
        attributes=attributes_cluster,
        is_run=True,
        is_root=False
    )
    Node(name=str(config_cluster), config=config_cluster, parent=root)

    build_tree(root)
    calc_tree(root)
