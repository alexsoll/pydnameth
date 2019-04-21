from pydnameth.config.experiment.types import DataType, Task, Method
from pydnameth.scripts.develop.table import table, table_aggregator
import copy
from anytree import Node
from pydnameth.config.config import Config
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.config.attributes.attributes import Observables, Cells, Attributes
from pydnameth.model.tree import build_tree, calc_tree


def residuals_common_table_linreg_dev(
    data,
    annotations,
    attributes,
    data_params,
):
    table(
        data=data,
        annotations=annotations,
        attributes=attributes,
        data_type=DataType.residuals_common,
        method=Method.linreg,
        data_params=data_params,
    )


def residuals_common_table_heteroscedasticity_dev(
    data,
    annotations,
    attributes,
    data_params,
):
    table(
        data=data,
        annotations=annotations,
        attributes=attributes,
        data_type=DataType.residuals_common,
        method=Method.heteroscedasticity,
        data_params=data_params,
    )


def residuals_common_table_aggregator_dev(
    data,
    annotations,
    attributes,
    observables_list,
    data_params,
):

    table_aggregator(
        DataType.residuals_common,
        data,
        annotations,
        attributes,
        observables_list,
        data_params=data_params,
    )


def residuals_common_table_aggregator_variance(
    data,
    annotations,
    attributes,
    observables_list,
    data_params,
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=DataType.residuals_common,
            task=Task.table,
            method=Method.aggregator,
            data_params=copy.deepcopy(data_params),
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
    )
    root = Node(name=str(config_root), config=config_root)

    for d in observables_list:
        observables_lvl_1 = Observables(
            name=copy.deepcopy(attributes.observables.name),
            types=d
        )

        cells_lvl_1 = Cells(
            name=copy.deepcopy(attributes.cells.name),
            types=copy.deepcopy(attributes.cells.types)
        )

        attributes_lvl_1 = Attributes(
            target=copy.deepcopy(attributes.target),
            observables=observables_lvl_1,
            cells=cells_lvl_1,
        )

        config_lvl_1 = Config(
            data=copy.deepcopy(data),
            experiment=Experiment(
                data=DataType.residuals_common,
                task=Task.table,
                method=Method.heteroscedasticity,
                data_params=copy.deepcopy(data_params),
                method_params={
                    'std_semi_window': 8
                }
            ),
            annotations=copy.deepcopy(annotations),
            attributes=attributes_lvl_1,
            is_run=True,
            is_root=False
        )
        Node(name=str(config_lvl_1), config=config_lvl_1, parent=root)

    observables_cluster = Observables(
        name=copy.deepcopy(attributes.observables.name),
        types={'gender': 'any'}
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
            data=DataType.betas,
            task=Task.table,
            method=Method.cluster,
            method_params={
                'eps': 0.2,
                'min_samples_percentage': 1
            }
        ),
        annotations=copy.deepcopy(annotations),
        attributes=attributes_cluster,
        is_run=True,
        is_root=False
    )
    Node(name=str(config_cluster), config=config_cluster, parent=root)

    build_tree(root)
    calc_tree(root)
