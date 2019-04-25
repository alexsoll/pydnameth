from pydnameth.config.experiment.types import DataType, Task, Method
from pydnameth.scripts.develop.table import table, table_aggregator, table_aggregator_variance
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
    table_aggregator_variance(
        DataType.residuals_common,
        data,
        annotations,
        attributes,
        observables_list,
        data_params=data_params,
    )

