import copy
from anytree import Node
from pydnameth.config.config import Config
from pydnameth.config.experiment.types import Task, Method
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.config.attributes.attributes import Observables, Cells, Attributes
from pydnameth.model.tree import build_tree, calc_tree


def table_linreg(
    data_type,
    data,
    annotations,
    attributes,
    data_params=None,
    task_params=None,
    method_params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=data_type,
            task=Task.table,
            method=Method.linreg,
            data_params=copy.deepcopy(data_params),
            task_params=copy.deepcopy(task_params),
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


def table_aggregator(
    data_type,
    data,
    annotations,
    attributes,
    observables_list,
    data_params=None,
    task_params=None,
    method_params=None
):
    child_methods_lvl_1 = [Method.polygon, Method.z_test_linreg]
    child_methods_lvl_2 = [Method.linreg]

    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=data_type,
            task=Task.table,
            method=Method.aggregator,
            data_params=copy.deepcopy(data_params),
            task_params=copy.deepcopy(task_params),
            method_params=copy.deepcopy(method_params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
    )
    root = Node(name=str(config_root), config=config_root)

    for child_method_lvl_1 in child_methods_lvl_1:
        config_lvl_1 = Config(
            data=copy.deepcopy(data),
            experiment=Experiment(
                data=data_type,
                task=Task.table,
                method=child_method_lvl_1,
                data_params=copy.deepcopy(data_params),
            ),
            annotations=copy.deepcopy(annotations),
            attributes=copy.deepcopy(attributes),
            is_run=True,
            is_root=False
        )
        node_lvl_1 = Node(name=str(config_lvl_1), config=config_lvl_1, parent=root)

        for child_method_lvl_2 in child_methods_lvl_2:
            for d in observables_list:
                observables_lvl_2 = Observables(
                    name=copy.deepcopy(attributes.observables.name),
                    types=d
                )

                cells_lvl_2 = Cells(
                    name=copy.deepcopy(attributes.cells.name),
                    types=copy.deepcopy(attributes.cells.types)
                )

                attributes_lvl_2 = Attributes(
                    target=copy.deepcopy(attributes.target),
                    observables=observables_lvl_2,
                    cells=cells_lvl_2,
                )

                config_lvl_2 = Config(
                    data=copy.deepcopy(data),
                    experiment=Experiment(
                        data=data_type,
                        task=Task.table,
                        method=copy.deepcopy(child_method_lvl_2),
                        data_params=copy.deepcopy(data_params),
                    ),
                    annotations=copy.deepcopy(annotations),
                    attributes=attributes_lvl_2,
                    is_run=True,
                    is_root=False
                )
                Node(name=str(config_lvl_2), config=config_lvl_2, parent=node_lvl_1)

    build_tree(root)
    calc_tree(root)
