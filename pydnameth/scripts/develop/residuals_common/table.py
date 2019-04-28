from pydnameth.config.experiment.types import DataType
from pydnameth.scripts.develop.table import table_aggregator_linreg, table_aggregator_variance


def residuals_common_table_aggregator_linreg(
    data,
    annotations,
    attributes,
    observables_list,
    data_params,
):
    table_aggregator_linreg(
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
