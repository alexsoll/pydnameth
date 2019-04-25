import copy
from anytree import Node
from pydnameth.config.config import Config
from pydnameth.config.experiment.types import Task, Method, DataType
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.config.attributes.attributes import Observables, Cells, Attributes
from pydnameth.model.tree import build_tree, calc_tree
from pydnameth.scripts.develop.table import table, table_aggregator, table_aggregator_variance


def betas_table_linreg_dev(
    data,
    annotations,
    attributes,
    method_params=None
):
    table(
        data=data,
        annotations=annotations,
        attributes=attributes,
        data_type=DataType.betas,
        method=Method.linreg,
        method_params=method_params,
    )


def betas_table_cluster_dev(
    data,
    annotations,
    attributes,
    method_params=None
):
    table(
        data=data,
        annotations=annotations,
        attributes=attributes,
        data_type=DataType.betas,
        method=Method.cluster,
        method_params=method_params,
    )


def betas_table_variance_linreg_dev(
    data,
    annotations,
    attributes,
    method_params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=DataType.betas,
            task=Task.table,
            method=Method.variance_linreg,
            method_params=copy.deepcopy(method_params)
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
    method_params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=DataType.betas,
            task=Task.table,
            method=Method.polygon,
            method_params=copy.deepcopy(method_params)
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
                data=DataType.betas,
                task=Task.table,
                method=copy.deepcopy(child_method)
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
    method_params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=DataType.betas,
            task=Task.table,
            method=Method.z_test_linreg,
            method_params=copy.deepcopy(method_params)
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
                data=DataType.betas,
                task=Task.table,
                method=copy.deepcopy(child_method)
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
    method_params=None
):
    table_aggregator(
        DataType.betas,
        data,
        annotations,
        attributes,
        observables_list,
        method_params
    )


def betas_table_aggregator_variance_dev(
    data,
    annotations,
    attributes,
    observables_list,
    data_params,
):
    table_aggregator_variance(
        DataType.betas,
        data,
        annotations,
        attributes,
        observables_list,
        data_params=data_params,
    )
