from pydnameth.config.experiment.types import DataType, Method
from pydnameth.scripts.develop.table import table, table_aggregator


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
