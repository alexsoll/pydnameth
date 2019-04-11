from pydnameth.config.experiment.types import DataType
from pydnameth.scripts.develop.table import table_linreg, table_aggregator


def residuals_special_table_linreg_dev(
    data,
    annotations,
    attributes,
    params=None
):
    table_linreg(
        DataType.residuals_special,
        data,
        annotations,
        attributes,
        params
    )


def residuals_special_table_aggregator_dev(
    data,
    annotations,
    attributes,
    observables_list,
    params=None
):
    table_aggregator(
        DataType.residuals_special,
        data,
        annotations,
        attributes,
        observables_list,
        params
    )
