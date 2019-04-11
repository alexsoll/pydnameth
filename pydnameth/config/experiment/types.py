from enum import Enum


class Task(Enum):
    table = 'table'
    clock = 'clock'
    plot = 'plot'
    observables = 'observables'
    methylation = 'methylation'

    def __str__(self):
        return str(self.value)


class Method(Enum):
    linreg = 'linreg'
    variance_linreg = 'variance_linreg'
    cluster = 'cluster'
    histogram = 'histogram'
    scatter = 'scatter'
    polygon = 'polygon'
    special = 'special'
    z_test_linreg = 'z_test_linreg'
    variance_histogram = 'variance_histogram'
    aggregator = 'aggregator'
    mock = 'mock'

    def __str__(self):
        return str(self.value)


class DataType(Enum):
    cpg = 'cpg'
    gene = 'gene'
    bop = 'bop'
    residuals_common = 'residuals_common'
    residuals_special = 'residuals_special'
    epimutations = 'epimutations'
    attributes = 'attributes'
    suppl = 'suppl'
    cache = 'cache'

    def __str__(self):
        return str(self.value)


def get_metrics_keys(setup):
    metrics = []

    if setup.task == Task.table:

        if setup.method == Method.linreg:
            metrics = [
                'item',
                'aux',
                'R2',
                'R2_adj',
                'f_stat',
                'prob(f_stat)',
                'log_likelihood',
                'AIC',
                'BIC',
                'omnibus',
                'prob(omnibus)',
                'skew',
                'kurtosis',
                'durbin_watson',
                'jarque_bera',
                'prob(jarque_bera)',
                'cond_no',
                'intercept',
                'slope',
                'intercept_std',
                'slope_std',
                'intercept_p_value',
                'slope_p_value',
                'normality_p_value_shapiro',
                'normality_p_value_ks_wo_params',
                'normality_p_value_ks_with_params',
                'normality_p_value_dagostino'
            ]
        elif setup.method == Method.variance_linreg:
            metrics = [
                'item',
                'aux',
                'R2',
                'intercept',
                'slope',
                'intercept_std',
                'slope_std',
                'intercept_p_value',
                'slope_p_value',
                'normality_p_value_shapiro',
                'normality_p_value_ks_wo_params',
                'normality_p_value_ks_with_params',
                'normality_p_value_dagostino',
                'R2_var',
                'intercept_var',
                'slope_var',
                'intercept_std_var',
                'slope_std_var',
                'intercept_p_value_var',
                'slope_p_value_var',
                'normality_p_value_shapiro_var',
                'normality_p_value_ks_wo_params_var',
                'normality_p_value_ks_with_params_var',
                'normality_p_value_dagostino_var'
            ]
        elif setup.method == Method.cluster:
            metrics = [
                'item',
                'aux',
                'number_of_clusters',
                'number_of_noise_points',
            ]
        elif setup.method == Method.polygon:
            metrics = [
                'item',
                'aux',
                'area_intersection_rel',
                'slope_intersection_rel',
                'max_abs_slope',
                'is_inside'
            ]
        elif setup.method == Method.special:
            metrics = [
                'item'
            ]
        elif setup.method == Method.z_test_linreg:
            metrics = [
                'item',
                'aux',
                'z_value',
                'p_value',
                'abs_z_value'
            ]
        elif setup.method == Method.aggregator:
            metrics = [
                'item',
                'aux'
            ]

    elif setup.task == Task.clock:

        if setup.method == Method.linreg:
            metrics = [
                'item',
                'aux',
                'R2',
                'r',
                'evs',
                'mae',
                'summary'
            ]

    return metrics


def get_main_metric(setup):
    metric = ()

    if setup.task == Task.table:

        if setup.method == Method.linreg:
            metric = ('R2', 'descending')
        elif setup.method == Method.variance_linreg:
            metric = ('R2_var', 'descending')
        elif setup.method == Method.cluster:
            metric = ('number_of_clusters', 'descending')
        elif setup.method == Method.polygon:
            metric = ('area_intersection_rel', 'ascending')
        elif setup.method == Method.z_test_linreg:
            metric = ('p_value', 'ascending')
        elif setup.method == Method.aggregator:
            metric = ('item', 'ascending')

    return metric
