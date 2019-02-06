from anytree import Node
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.config.experiment.types import DataType, Task, Method
from pydnameth.config.config import Config
from pydnameth.model.tree import calc_tree
from pydnameth.config.attributes.attributes import Attributes, Observables, Cells


def cpg_proc_table_linreg(
    data,
    annotations,
    attributes
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

    :param data: pdm.Data instance, which specifies information about dataset.
    :param annotations: pdm.Annotations instance, which specifies subset of CpGs.
    :param attributes: pdm.Attributes instance, which specifies information about subjects.
    """
    config_root = Config(
        data=data,
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=Method.linreg,
            params={}
        ),
        annotations=annotations,
        attributes=attributes
    )

    root = Node(name=str(config_root), config=config_root)
    calc_tree(root)


def cpg_proc_table_variance_linreg(
    data,
    annotations,
    attributes
):
    """
    Producing table with information for linear regression of variance from primary linear regression between target observable
    and methylation level for each CpG.

    Each row corresponds to specific CpG.

    Columns:

    * item: CpG id.
    * aux: gene, on which CpG is mapped.
    * R2: determination coefficient of primary linear regression.
      A statistical measure of how well the regression line approximates the data points.
    * intercept: estimated value of the intercept of primary linear regression.
    * slope: estimated value of the slope of primary linear regression.
    * intercept_std: standard error of the estimate of the intercept of primary linear regression.
    * slope_std: standard error of the estimate of the slope of primary linear regression.
    * intercept_p_value: p-value for the intercept of primary linear regression.
    * slope_p_pvalue: p-value for the slope of primary linear regression.
    * R2_var: determination coefficient of linear regression for variance.
      A statistical measure of how well the regression line approximates the data points.
    * intercept_var: estimated value of the intercept of linear regression for variance.
    * slope_var: estimated value of the slope of linear regression for variance.
    * intercept_std_var: standard error of the estimate of the intercept of linear regression for variance.
    * slope_std_var: standard error of the estimate of the slope of linear regression for variance.
    * intercept_p_value_var: p-value for the intercept of linear regression for variance.
    * slope_p_pvalue_var: p-value for the slope of linear regression for variance.

    :param data: pdm.Data instance, which specifies information about dataset.
    :param annotations: pdm.Annotations instance, which specifies subset of CpGs.
    :param attributes: pdm.Attributes instance, which specifies information about subjects.
    """
    config_root = Config(
        data=data,
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=Method.variance_linreg,
            params={}
        ),
        annotations=annotations,
        attributes=attributes
    )

    root = Node(name=str(config_root), config=config_root)
    calc_tree(root)


def cpg_proc_table_polygon(
    data,
    annotations,
    attributes,
    observables_list,
    child_method=Method.linreg
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

    * R2_***: determination coefficient. A statistical measure of how well the regression line approximates the data points.
    * intercept_***: estimated value of the intercept of linear regression.
    * slope_***: estimated value of the slope of linear regression.
    * intercept_std_***: standard error of the estimate of the intercept of linear regression.
    * slope_std_***: standard error of the estimate of the slope of linear regression.
    * intercept_p_value_***: p-value for the intercept of linear regression.
    * slope_p_pvalue_***: p-value for the slope of linear regression.

    Where *** is the name of subjects subset.

    :param data: pdm.Data instance, which specifies information about dataset.
    :param annotations: pdm.Annotations instance, which specifies subset of CpGs.
    :param attributes: pdm.Attributes instance, which specifies information about subjects.
    :param observables_list: list of subjects subsets. Each element in list is dict,
     where ``key`` is observable name and ``value`` is possible values for this observable.
    """
    config_root = Config(
        data=data,
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=Method.polygon,
            params={}
        ),
        annotations=annotations,
        attributes=attributes
    )
    root = Node(name=str(config_root), config=config_root)

    for d in observables_list:
        observables_child = Observables(
            name=attributes.observables.name,
            types=d
        )

        cells_child = Cells(
            name=attributes.cells.name,
            types=attributes.cells.types
        )

        attributes_child = Attributes(
            target=attributes.target,
            observables=observables_child,
            cells=cells_child,
        )

        config_child = Config(
            data=data,
            experiment=Experiment(
                type=DataType.cpg,
                task=Task.table,
                method=child_method,
                params={}
            ),
            annotations=annotations,
            attributes=attributes_child
        )
        Node(name=str(config_child), config=config_child, parent=root)

    calc_tree(root)


def cpg_proc_table_z_test_linreg(
    data,
    annotations,
    attributes,
    observables_list,
    child_method=Method.linreg
):
    """
    Producing table with information about z-test for slopes of linear regression performed for each subset separately.

    Each row corresponds to specific CpG.

    Columns:

    * item: CpG id.
    * aux: gene, on which CpG is mapped.
    * z_value: number of standard deviations by which data point is above the mean value.
      The considered data point is the difference between two linear regressions slopes.
    * p_value: probability of rejecting the null hypothesis that the difference in slopes is zero.

    For each subjects subset the next columns are added to the resulting table:

    * R2_***: determination coefficient. A statistical measure of how well the regression line approximates the data points.
    * intercept_***: estimated value of the intercept of linear regression.
    * slope_***: estimated value of the slope of linear regression.
    * intercept_std_***: standard error of the estimate of the intercept of linear regression.
    * slope_std_***: standard error of the estimate of the slope of linear regression.
    * intercept_p_value_***: p-value for the intercept of linear regression.
    * slope_p_pvalue_***: p-value for the slope of linear regression.

    Where *** is the name of subjects subset.

    :param data: pdm.Data instance, which specifies information about dataset.
    :param annotations: pdm.Annotations instance, which specifies subset of CpGs.
    :param attributes: pdm.Attributes instance, which specifies information about subjects.
    :param observables_list: list of subjects subsets. Each element in list is dict,
     where ``key`` is observable name and ``value`` is possible values for this observable.
    """
    config_root = Config(
        data=data,
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=Method.z_test_linreg,
            params={}
        ),
        annotations=annotations,
        attributes=attributes
    )
    root = Node(name=str(config_root), config=config_root)

    for d in observables_list:
        observables_child = Observables(
            name=attributes.observables.name,
            types=d
        )

        cells_child = Cells(
            name=attributes.cells.name,
            types=attributes.cells.types
        )

        attributes_child = Attributes(
            target=attributes.target,
            observables=observables_child,
            cells=cells_child,
        )

        config_child = Config(
            data=data,
            experiment=Experiment(
                type=DataType.cpg,
                task=Task.table,
                method=child_method,
                params={}
            ),
            annotations=annotations,
            attributes=attributes_child
        )
        Node(name=str(config_child), config=config_child, parent=root)

    calc_tree(root)


def cpg_proc_clock_linreg(
    data,
    annotations,
    attributes,
    child_method=Method.linreg
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
    * summary: summary output from OLS

    :param data: pdm.Data instance, which specifies information about dataset.
    :param annotations: pdm.Annotations instance, which specifies subset of CpGs.
    :param attributes: pdm.Attributes instance, which specifies information about subjects.
    """
    config_root = Config(
        data=data,
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.clock,
            method=Method.linreg,
            params={}
        ),
        annotations=annotations,
        attributes=attributes
    )
    root = Node(name=str(config_root), config=config_root)

    config_child = Config(
        data=data,
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=child_method,
            params={}
        ),
        annotations=annotations,
        attributes=attributes
    )

    Node(name=str(config_child), config=config_child, parent=root)

    calc_tree(root)


def cpg_plot_methylation_scatter(
    data,
    annotations,
    attributes,
    cpg_list,
    observables_list,
    child_method=Method.linreg
):
    """
    Plotting methylation level from observables as scatter for provided subjects subsets and provided CpG list.

    :param data: pdm.Data instance, which specifies information about dataset.
    :param annotations: pdm.Annotations instance, which specifies subset of CpGs.
    :param attributes: pdm.Attributes instance, which specifies information about subjects.
    :param cpg_list: List of CpGs for plotting
    :param observables_list: list of subjects subsets. Each element in list is dict,
     where ``key`` is observable name and ``value`` is possible values for this observable.
    """
    for cpg in cpg_list:

        config_root = Config(
            data=data,
            experiment=Experiment(
                type=DataType.cpg,
                task=Task.methylation,
                method=Method.scatter,
                params={}
            ),
            annotations=annotations,
            attributes=attributes
        )
        config_root.experiment.params['item'] = cpg

        root = Node(name=str(config_root), config=config_root)

        for d in observables_list:
            observables_child = Observables(
                name=attributes.observables.name,
                types=d
            )

            cells_child = Cells(
                name=attributes.cells.name,
                types=attributes.cells.types
            )

            attributes_child = Attributes(
                target=attributes.target,
                observables=observables_child,
                cells=cells_child,
            )

            config_child = Config(
                data=data,
                experiment=Experiment(
                    type=DataType.cpg,
                    task=Task.table,
                    method=child_method,
                    params={}
                ),
                annotations=annotations,
                attributes=attributes_child,
                is_run=False
            )
            Node(name=str(config_child), config=config_child, parent=root)

        calc_tree(root)


def attributes_plot_observables_histogram(
    data,
    annotations,
    attributes,
    observables_list,
):
    """
    Plotting histogram for target observable distribution for provided subjects subsets and provided CpG list.

    :param data: pdm.Data instance, which specifies information about dataset.
    :param annotations: pdm.Annotations instance, which specifies subset of CpGs.
    :param attributes: pdm.Attributes instance, which specifies information about subjects.
    :param cpg_list: List of CpGs for plotting
    :param observables_list: list of subjects subsets. Each element in list is dict,
     where ``key`` is observable name and ``value`` is possible values for this observable.
    """
    config_root = Config(
        data=data,
        experiment=Experiment(
            type=DataType.attributes,
            task=Task.observables,
            method=Method.histogram,
            params={}
        ),
        annotations=annotations,
        attributes=attributes
    )
    root = Node(name=str(config_root), config=config_root)

    for d in observables_list:
        observables_child = Observables(
            name=attributes.observables.name,
            types=d
        )

        cells_child = Cells(
            name=attributes.cells.name,
            types=attributes.cells.types
        )

        attributes_child = Attributes(
            target=attributes.target,
            observables=observables_child,
            cells=cells_child,
        )

        config_child = Config(
            data=data,
            experiment=config_root.experiment,
            annotations=annotations,
            attributes=attributes_child,
            is_run=False
        )
        Node(name=str(config_child), config=config_child, parent=root)

    calc_tree(root)
