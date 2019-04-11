from pydnameth.config.experiment.types import Method
from pydnameth.scripts.develop.betas.clock import betas_clock_linreg_dev


def betas_clock_linreg(
    data,
    annotations,
    attributes,
    params=None
):
    """
    Producing epigentic clock, using best CpGs target-predictors.

    Firstly, produce linear regression between target observable
    and methylation level to define best CpGs target-predictors, which are at the top of table.

    Secondly, produce epigentic clock.

    Epigentic clock represents as table:
    Each row corresponds to clocks, which are built on all CpGs from the previous rows including the current row.
    Columns:

    * item: CpG id.
    * aux: gene, on which CpG is mapped.
    * R2: determination coefficient of linear regression between real and predicted target observable.
      A statistical measure of how well the regression line approximates the data points.
    * r: correlation coefficient of linear regression between real and predicted target observable.
    * evs: explained variance regression score.
    * mae: mean absolute error regression loss.
    * summary: summary output from OLS.

    Possible parameters of experiment:

    * ``'type'``: type of clocks. \n
      Possible options: \n
      ``'all'``: iterative building of clocks starting from one element in the model,
      ending with ``'size'`` elements in the model. \n
      ``'single '``: building of clocks only with ``'size'`` elements in the model. \n
      ``'deep'``: iterative building of clocks starting from one element in the model,
      ending with ``'size'`` elements in the model, but choosing all posible combinations from ``'size'`` elements.
    * ``'part'``: the proportion of considered number of subject in the test set. From ``0.0`` to ``1.0``.
    * ``'size'``: maximum number of exogenous variables in a model.
    * ``'runs'`` number of bootstrap runs in model

    :param data: pdm.Data instance, which specifies information about dataset.
    :param annotations: pdm.Annotations instance, which specifies subset of CpGs.
    :param attributes: pdm.Attributes instance, which specifies information about subjects.
    :param params: parameters of experiment.
    """

    child_method = Method.linreg

    betas_clock_linreg_dev(
        data=data,
        annotations=annotations,
        attributes=attributes,
        child_method=child_method,
        params=params
    )
