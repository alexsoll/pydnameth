from pydnameth.config.experiment.types import DataType
from pydnameth.scripts.develop.table import table_linreg, table_aggregator


def residuals_common_table_linreg_dev(
    data,
    annotations,
    attributes,
    data_params,
):
    table_linreg(
        DataType.residuals_common,
        data,
        annotations,
        attributes,
        data_params=data_params
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
