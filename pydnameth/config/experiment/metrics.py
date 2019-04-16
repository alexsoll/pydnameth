from pydnameth import DataType, Task, Method


def get_method_metrics_keys(config):
    metrics = []

    if config.experiment.data in [DataType.betas, DataType.residuals_common, DataType.residuals_special]:

        if config.experiment.task == Task.table:

            if config.experiment.method == Method.linreg:

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

            elif config.experiment.method == Method.variance_linreg:

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

            elif config.experiment.method == Method.cluster:

                metrics = [
                    'item',
                    'aux',
                    'number_of_clusters',
                    'number_of_noise_points',
                ]

            elif config.experiment.method == Method.polygon:

                metrics = [
                    'item',
                    'aux',
                    'area_intersection_rel',
                    'slope_intersection_rel',
                    'max_abs_slope',
                    'is_inside'
                ]

            elif config.experiment.method == Method.special:

                metrics = [
                    'item'
                ]

            elif config.experiment.method == Method.z_test_linreg:

                metrics = [
                    'item',
                    'aux',
                    'z_value',
                    'p_value',
                    'abs_z_value'
                ]

            elif config.experiment.method == Method.aggregator:

                metrics = [
                    'item',
                    'aux'
                ]

        elif config.experiment.task == Task.clock:

            if config.experiment.method == Method.linreg:
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
