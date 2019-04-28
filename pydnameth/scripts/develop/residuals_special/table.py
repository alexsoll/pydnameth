from pydnameth.config.experiment.types import DataType
from pydnameth.scripts.develop.table import table_aggregator_linreg


def residuals_special_table_aggregator(
    data,
    annotations,
    attributes,
    observables_list,
    data_params,
):
    table_aggregator_linreg(
        DataType.residuals_special,
        data,
        annotations,
        attributes,
        observables_list,
        data_params=data_params,
    )
