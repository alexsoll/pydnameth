from pydnameth.config.experiment.types import DataType, Method
from pydnameth.scripts.develop.table import table, table_aggregator


def residuals_special_table_linreg_dev(
    data,
    annotations,
    attributes,
    data_params,
):
    table(
        data=data,
        annotations=annotations,
        attributes=attributes,
        data_type=DataType.residuals_special,
        method=Method.linreg,
        data_params=data_params,
    )


def residuals_special_table_aggregator_dev(
    data,
    annotations,
    attributes,
    observables_list,
    data_params,
):
    table_aggregator(
        DataType.residuals_special,
        data,
        annotations,
        attributes,
        observables_list,
        data_params=data_params,
    )
