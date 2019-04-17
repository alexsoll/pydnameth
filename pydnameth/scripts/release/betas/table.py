from pydnameth.config.experiment.types import Method
from pydnameth.scripts.develop.betas.table import \
    betas_table_linreg_dev, \
    betas_table_polygon_dev, \
    betas_table_z_test_linreg_dev


def cpg_proc_table_linreg(
    data,
    annotations,
    attributes,
    params=None
):
    """
    Producing table with information for linear regression between target observable
    and methylation level for each CpG.

    Each row corresponds to specific CpG.

    Columns:

    * item: CpG id.
    * aux: gene, on which CpG is mapped.
    * R2: determination coefficient. A statistical measure of how well the regression line approximates the data points.
    * intercept: estimated value of the intercept of linear regression.
    * slope: estimated value of the slope of linear regression.
    * intercept_std: standard error of the estimate of the intercept of linear regression.
    * slope_std: standard error of the estimate of the slope of linear regression.
    * intercept_p_value: p-value for the intercept of linear regression.
    * slope_p_pvalue: p-value for the slope of linear regression.

    Possible parameters of experiment:

    * None

    :param data: pdm.Data instance, which specifies information about dataset.
    :param annotations: pdm.Annotations instance, which specifies subset of CpGs.
    :param attributes: pdm.Attributes instance, which specifies information about subjects.
    :param params: parameters of experiment.
    """
    betas_table_linreg_dev(
        data=data,
        annotations=annotations,
        attributes=attributes,
        method_params=params
    )


def cpg_proc_table_polygon(
    data,
    annotations,
    attributes,
    observables_list,
    params=None
):
    """
    Producing table with information about observable-specificity of methylation level
    and target observable for each CpG using result of linear regression performed for each subset separately.

    Firstly, for each subjects subset creates polygon.

    Secondly, intersection of all of polygons analyzed and linear regression characteristics analyzed.

    Each row corresponds to specific CpG.

    Columns:

    * item: CpG id.
    * aux: gene, on which CpG is mapped.
    * area_intersection_rel: relative intersection area of polygons
      which is equals area of polygon(s) intersection to area of polygons union ratio.
    * slope_intersection_rel: relative intersection area of allowed regions for slopes of linear regression.
    * max_abs_slope: maximal absolute slope between all provided subjects subsets

    For each subjects subset the next columns are added to the resulting table:

    * R2_***: determination coefficient.
      A statistical measure of how well the regression line approximates the data points.
    * intercept_***: estimated value of the intercept of linear regression.
    * slope_***: estimated value of the slope of linear regression.
    * intercept_std_***: standard error of the estimate of the intercept of linear regression.
    * slope_std_***: standard error of the estimate of the slope of linear regression.
    * intercept_p_value_***: p-value for the intercept of linear regression.
    * slope_p_pvalue_***: p-value for the slope of linear regression.

    Where *** is the name of subjects subset.

    Possible parameters of experiment:

    * None

    :param data: pdm.Data instance, which specifies information about dataset.
    :param annotations: pdm.Annotations instance, which specifies subset of CpGs.
    :param attributes: pdm.Attributes instance, which specifies information about subjects.
    :param observables_list: list of subjects subsets. Each element in list is dict,
     where ``key`` is observable name and ``value`` is possible values for this observable.
    :param params: parameters of experiment.
    """

    child_method = Method.linreg

    betas_table_polygon_dev(
        data=data,
        annotations=annotations,
        attributes=attributes,
        observables_list=observables_list,
        child_method=child_method,
        method_params=params
    )


def cpg_proc_table_z_test_linreg(
    data,
    annotations,
    attributes,
    observables_list,
    params=None
):
    """
    Producing table with information about z-test for slopes of linear regression performed for each subset separately.

    Each row corresponds to specific CpG.

    Columns:

    * item: CpG id.
    * aux: gene, on which CpG is mapped.
    * z_value: number of standard deviations by which data point is above the mean value.
      The considered data point is the difference between two linear regressions slopes.
    * abs_z_value: absolute z_value
    * p_value: probability of rejecting the null hypothesis that the difference in slopes is zero.

    For each subjects subset the next columns are added to the resulting table:

    * R2_***: determination coefficient.
    * A statistical measure of how well the regression line approximates the data points.
    * intercept_***: estimated value of the intercept of linear regression.
    * slope_***: estimated value of the slope of linear regression.
    * intercept_std_***: standard error of the estimate of the intercept of linear regression.
    * slope_std_***: standard error of the estimate of the slope of linear regression.
    * intercept_p_value_***: p-value for the intercept of linear regression.
    * slope_p_pvalue_***: p-value for the slope of linear regression.

    Where *** is the name of subjects subset.

    Possible parameters of experiment:

    * None

    :param data: pdm.Data instance, which specifies information about dataset.
    :param annotations: pdm.Annotations instance, which specifies subset of CpGs.
    :param attributes: pdm.Attributes instance, which specifies information about subjects.
    :param observables_list: list of subjects subsets. Each element in list is dict,
     where ``key`` is observable name and ``value`` is possible values for this observable.
     :param params: parameters of experiment.
    """

    child_method = Method.linreg

    betas_table_z_test_linreg_dev(
        data=data,
        annotations=annotations,
        attributes=attributes,
        observables_list=observables_list,
        child_method=child_method,
        method_params=params
    )
