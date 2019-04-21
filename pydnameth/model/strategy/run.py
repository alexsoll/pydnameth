import abc
from pydnameth.config.experiment.types import Method, DataType
from pydnameth.config.experiment.metrics import get_method_metrics_keys
import statsmodels.api as sm
import statsmodels.stats.diagnostic as ssd
import numpy as np
from sklearn.cluster import DBSCAN
from pydnameth.routines.clock.types import ClockExogType, Clock
from pydnameth.routines.clock.linreg.processing import build_clock_linreg
import plotly.graph_objs as go
import colorlover as cl
from shapely import geometry
from scipy.stats import norm, shapiro, kstest, normaltest
from pydnameth.routines.common import is_float, get_names, normalize_to_0_1
from pydnameth.routines.polygon.types import PolygonRoutines
from statsmodels.stats.stattools import jarque_bera, omni_normtest, durbin_watson
from tqdm import tqdm
from pydnameth.routines.residuals.variance import residuals_variance


class RunStrategy(metaclass=abc.ABCMeta):

    def __init__(self, get_strategy):
        self.get_strategy = get_strategy

    @abc.abstractmethod
    def single(self, item, config, configs_child):
        pass

    @abc.abstractmethod
    def iterate(self, config, configs_child):
        pass

    @abc.abstractmethod
    def run(self, config, configs_child):
        pass


class TableRunStrategy(RunStrategy):

    def single(self, item, config, configs_child):

        if config.experiment.data in [DataType.betas, DataType.betas_adj, DataType.residuals_common, DataType.residuals_special]:

            if config.experiment.method == Method.linreg:

                targets = self.get_strategy.get_target(config)
                x = sm.add_constant(targets)
                y = self.get_strategy.get_single_base(config, [item])[0]

                results = sm.OLS(y, x).fit()

                residuals = results.resid

                jb, jbpv, skew, kurtosis = jarque_bera(results.wresid)
                omni, omnipv = omni_normtest(results.wresid)

                res_mean = np.mean(residuals)
                res_std = np.std(residuals)

                _, normality_p_value_shapiro = shapiro(residuals)
                _, normality_p_value_ks_wo_params = kstest(residuals, 'norm')
                _, normality_p_value_ks_with_params = kstest(residuals, 'norm', (res_mean, res_std))
                _, normality_p_value_dagostino = normaltest(residuals)

                config.metrics['item'].append(item)
                aux = self.get_strategy.get_aux(config, item)
                config.metrics['aux'].append(aux)
                config.metrics['R2'].append(results.rsquared)
                config.metrics['R2_adj'].append(results.rsquared_adj)
                config.metrics['f_stat'].append(results.fvalue)
                config.metrics['prob(f_stat)'].append(results.f_pvalue)
                config.metrics['log_likelihood'].append(results.llf)
                config.metrics['AIC'].append(results.aic)
                config.metrics['BIC'].append(results.bic)
                config.metrics['omnibus'].append(omni)
                config.metrics['prob(omnibus)'].append(omnipv)
                config.metrics['skew'].append(skew)
                config.metrics['kurtosis'].append(kurtosis)
                config.metrics['durbin_watson'].append(durbin_watson(results.wresid))
                config.metrics['jarque_bera'].append(jb)
                config.metrics['prob(jarque_bera)'].append(jbpv)
                config.metrics['cond_no'].append(results.condition_number)
                config.metrics['normality_p_value_shapiro'].append(normality_p_value_shapiro)
                config.metrics['normality_p_value_ks_wo_params'].append(normality_p_value_ks_wo_params)
                config.metrics['normality_p_value_ks_with_params'].append(normality_p_value_ks_with_params)
                config.metrics['normality_p_value_dagostino'].append(normality_p_value_dagostino)
                config.metrics['intercept'].append(results.params[0])
                config.metrics['slope'].append(results.params[1])
                config.metrics['intercept_std'].append(results.bse[0])
                config.metrics['slope_std'].append(results.bse[1])
                config.metrics['intercept_p_value'].append(results.pvalues[0])
                config.metrics['slope_p_value'].append(results.pvalues[1])

            elif config.experiment.method == Method.variance_linreg:

                targets = self.get_strategy.get_target(config)
                x = sm.add_constant(targets)
                y = self.get_strategy.get_single_base(config, [item])[0]

                results = sm.OLS(y, x).fit()
                residuals = results.resid

                res_mean = np.mean(residuals)
                res_std = np.std(residuals)

                _, normality_p_value_shapiro = shapiro(residuals)
                _, normality_p_value_ks_wo_params = kstest(residuals, 'norm')
                _, normality_p_value_ks_with_params = kstest(residuals, 'norm', (res_mean, res_std))
                _, normality_p_value_dagostino = normaltest(residuals)

                config.metrics['item'].append(item)
                aux = self.get_strategy.get_aux(config, item)
                config.metrics['aux'].append(aux)
                config.metrics['R2'].append(results.rsquared)
                config.metrics['intercept'].append(results.params[0])
                config.metrics['slope'].append(results.params[1])
                config.metrics['intercept_std'].append(results.bse[0])
                config.metrics['slope_std'].append(results.bse[1])
                config.metrics['intercept_p_value'].append(results.pvalues[0])
                config.metrics['slope_p_value'].append(results.pvalues[1])
                config.metrics['normality_p_value_shapiro'].append(normality_p_value_shapiro)
                config.metrics['normality_p_value_ks_wo_params'].append(normality_p_value_ks_wo_params)
                config.metrics['normality_p_value_ks_with_params'].append(normality_p_value_ks_with_params)
                config.metrics['normality_p_value_dagostino'].append(normality_p_value_dagostino)

                diffs = np.abs(residuals)

                results_var = sm.OLS(diffs, x).fit()
                residuals_var = results_var.resid

                res_mean_var = np.mean(residuals_var)
                res_std_var = np.std(residuals_var)

                _, normality_p_value_shapiro_var = shapiro(residuals_var)
                _, normality_p_value_ks_wo_params_var = kstest(residuals_var, 'norm')
                _, normality_p_value_ks_with_params_var = kstest(residuals_var, 'norm', (res_mean_var, res_std_var))
                _, normality_p_value_dagostino_var = normaltest(residuals_var)

                config.metrics['R2_var'].append(results_var.rsquared)
                config.metrics['intercept_var'].append(results_var.params[0])
                config.metrics['slope_var'].append(results_var.params[1])
                config.metrics['intercept_std_var'].append(results_var.bse[0])
                config.metrics['slope_std_var'].append(results_var.bse[1])
                config.metrics['intercept_p_value_var'].append(results_var.pvalues[0])
                config.metrics['slope_p_value_var'].append(results_var.pvalues[1])
                config.metrics['normality_p_value_shapiro_var'].append(normality_p_value_shapiro_var)
                config.metrics['normality_p_value_ks_wo_params_var'].append(normality_p_value_ks_wo_params_var)
                config.metrics['normality_p_value_ks_with_params_var'].append(normality_p_value_ks_with_params_var)
                config.metrics['normality_p_value_dagostino_var'].append(normality_p_value_dagostino_var)

            elif config.experiment.method == Method.cluster:

                x = self.get_strategy.get_target(config)
                x_normed = normalize_to_0_1(x)
                y = self.get_strategy.get_single_base(config, [item])[0]
                y_normed = normalize_to_0_1(y)

                min_samples = max(1, int(config.experiment.method_params['min_samples_percentage'] * len(x) / 100.0))

                X = np.array([x_normed, y_normed]).T
                db = DBSCAN(eps=config.experiment.method_params['eps'], min_samples=min_samples).fit(X)
                core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
                core_samples_mask[db.core_sample_indices_] = True
                labels = db.labels_
                number_of_clusters = len(set(labels)) - (1 if -1 in labels else 0)
                number_of_noise_points = list(labels).count(-1)

                config.metrics['item'].append(item)
                config.metrics['aux'].append(self.get_strategy.get_aux(config, item))
                config.metrics['number_of_clusters'].append(number_of_clusters)
                config.metrics['number_of_noise_points'].append(number_of_noise_points)

            elif config.experiment.method == Method.polygon:

                polygons_region = []
                polygons_slope = []
                polygons_region_min = []
                max_abs_slope = 0.0
                is_inside = False

                mins = [min(self.get_strategy.get_target(config_child)) for config_child in configs_child]
                maxs = [max(self.get_strategy.get_target(config_child)) for config_child in configs_child]
                border_l = max(mins)
                border_r = min(maxs)
                if border_l > border_r:
                    raise ValueError('Polygons borders are not consistent')

                metrics_keys = get_method_metrics_keys(config)

                for config_child in configs_child:

                    targets = self.get_strategy.get_target(config_child)
                    item_id = config_child.advanced_dict[item]

                    for key in config_child.advanced_data:
                        if key not in metrics_keys:
                            advanced_data = config_child.advanced_data[key][item_id]
                            suffix = str(config_child.attributes.observables)
                            if suffix != '' and suffix not in key:
                                key += '_' + suffix
                            config.metrics[key].append(advanced_data)
                            metrics_keys.append(key)

                    points_region = []
                    points_slope = []
                    points_region_min = []

                    if config_child.experiment.method == Method.linreg:

                        intercept = config_child.advanced_data['intercept'][item_id]
                        slope = config_child.advanced_data['slope'][item_id]
                        intercept_std = config_child.advanced_data['intercept_std'][item_id]
                        slope_std = config_child.advanced_data['slope_std'][item_id]

                        pr = PolygonRoutines(
                            x=targets,
                            y=[],
                            params={
                                'intercept': intercept,
                                'slope': slope,
                                'intercept_std': intercept_std,
                                'slope_std': slope_std
                            },
                            method=config_child.experiment.method
                        )
                        points_region = pr.get_border_points()

                        points_slope = [
                            geometry.Point(slope - 3.0 * slope_std, 0.0),
                            geometry.Point(slope + 3.0 * slope_std, 0.0),
                            geometry.Point(slope + 3.0 * slope_std, 1.0),
                            geometry.Point(slope - 3.0 * slope_std, 1.0),
                        ]

                        max_abs_slope = max(max_abs_slope, abs(slope))

                        pr_min = PolygonRoutines(
                            x=[border_l, border_r],
                            y=[],
                            params={
                                'intercept': intercept,
                                'slope': slope,
                                'intercept_std': intercept_std,
                                'slope_std': slope_std
                            },
                            method=config_child.experiment.method
                        )
                        points_region_min = pr_min.get_border_points()

                    elif config_child.experiment.method == Method.linreg.variance_linreg:

                        intercept = config_child.advanced_data['intercept'][item_id]
                        slope = config_child.advanced_data['slope'][item_id]
                        slope_std = config_child.advanced_data['slope_std'][item_id]
                        intercept_var = config_child.advanced_data['intercept_var'][item_id]
                        slope_var = config_child.advanced_data['slope_var'][item_id]

                        pr = PolygonRoutines(
                            x=targets,
                            y=[],
                            params={
                                'intercept': intercept,
                                'slope': slope,
                                'intercept_var': intercept_var,
                                'slope_var': slope_var,
                            },
                            method=config_child.experiment.method
                        )

                        points_region = pr.get_border_points()

                        points_slope = [
                            geometry.Point(slope - 3.0 * slope_std, 0.0),
                            geometry.Point(slope + 3.0 * slope_std, 0.0),
                            geometry.Point(slope + 3.0 * slope_std, 1.0),
                            geometry.Point(slope - 3.0 * slope_std, 1.0),
                        ]

                        max_abs_slope = max(max_abs_slope, abs(slope))

                    polygon = geometry.Polygon([[point.x, point.y] for point in points_region])
                    polygons_region.append(polygon)

                    polygon = geometry.Polygon([[point.x, point.y] for point in points_slope])
                    polygons_slope.append(polygon)

                    polygon = geometry.Polygon([[point.x, point.y] for point in points_region_min])
                    polygons_region_min.append(polygon)

                intersection = polygons_region[0]
                union = polygons_region[0]
                for polygon in polygons_region[1::]:
                    intersection = intersection.intersection(polygon)
                    union = union.union(polygon)
                area_intersection_rel = intersection.area / union.area

                union = polygons_region_min[0]
                for polygon in polygons_region_min[1::]:
                    union = union.union(polygon)
                for polygon in polygons_region_min:
                    if union.area == polygon.area:
                        is_inside = True

                intersection = polygons_slope[0]
                union = polygons_slope[0]
                for polygon in polygons_slope[1::]:
                    intersection = intersection.intersection(polygon)
                    union = union.union(polygon)
                slope_intersection_rel = intersection.area / union.area

                config.metrics['item'].append(item)
                aux = self.get_strategy.get_aux(config, item)
                config.metrics['aux'].append(aux)
                config.metrics['area_intersection_rel'].append(area_intersection_rel)
                config.metrics['slope_intersection_rel'].append(slope_intersection_rel)
                config.metrics['max_abs_slope'].append(max_abs_slope)
                config.metrics['is_inside'].append(is_inside)

            elif config.experiment.method == Method.z_test_linreg:

                slopes = []
                slopes_std = []
                num_subs = []

                metrics_keys = get_method_metrics_keys(config)

                for config_child in configs_child:

                    item_id = config_child.advanced_dict[item]

                    for key in config_child.advanced_data:
                        if key not in metrics_keys:
                            advanced_data = config_child.advanced_data[key][item_id]
                            suffix = str(config_child.attributes.observables)
                            if suffix != '' and suffix not in key:
                                key += '_' + suffix
                            config.metrics[key].append(advanced_data)
                            metrics_keys.append(key)

                    slopes.append(config_child.advanced_data['slope'][item_id])
                    slopes_std.append(config_child.advanced_data['slope_std'][item_id])
                    num_subs.append(len(config_child.attributes_dict['age']))

                std_errors = [slopes_std[i] / np.sqrt(num_subs[i]) for i in range(0, len(slopes_std))]
                z_value = (slopes[0] - slopes[1]) / np.sqrt(sum([std_error * std_error for std_error in std_errors]))
                p_value = norm.sf(abs(z_value)) * 2.0

                config.metrics['item'].append(item)
                aux = self.get_strategy.get_aux(config, item)
                config.metrics['aux'].append(aux)
                config.metrics['z_value'].append(z_value)
                config.metrics['p_value'].append(p_value)
                config.metrics['abs_z_value'].append(np.absolute(z_value))

            elif config.experiment.method == Method.aggregator:

                metrics_keys = get_method_metrics_keys(config)

                for config_child in configs_child:

                    item_id = config_child.advanced_dict[item]

                    for key in config_child.advanced_data:
                        if key not in metrics_keys:
                            advanced_data = config_child.advanced_data[key][item_id]
                            suffix = str(config_child.attributes.observables)
                            if suffix != '' and suffix not in key:
                                key += '_' + suffix
                            config.metrics[key].append(advanced_data)
                            metrics_keys.append(key)

                config.metrics['item'].append(item)
                aux = self.get_strategy.get_aux(config, item)
                config.metrics['aux'].append(aux)

        if config.experiment.data in [DataType.residuals_common, DataType.residuals_special]:

            if config.experiment.method == Method.heteroscedasticity:

                targets = np.asarray(self.get_strategy.get_target(config)).reshape(-1, 1)
                residuals = self.get_strategy.get_single_base(config, [item]).reshape(-1, 1)

                gq_test = ssd.het_goldfeldquandt(residuals, targets)

                targets = np.squeeze(np.asarray(targets))
                residuals = np.squeeze(np.asarray(residuals))

                exog = sm.add_constant(targets)
                endog = residuals
                results = sm.OLS(endog, exog).fit()
                residuals_upd = results.resid

                std_semi_window = config.experiment.method_params['std_semi_window']
                std_exog, std_endog = residuals_variance(targets, residuals_upd, std_semi_window)

                std_lin_exog = sm.add_constant(std_exog)
                std_lin_endog = std_endog
                std_lin_results = sm.OLS(std_lin_endog, std_lin_exog).fit()

                std_log_exog = sm.add_constant(std_exog)
                std_log_endog = np.log(std_endog)
                std_log_results = sm.OLS(std_log_endog, std_log_exog).fit()

                R2s = [std_lin_results.rsquared, std_log_results.rsquared]
                best_R2_id = np.argmax(R2s)

                R2s_adj = [std_lin_results.rsquared_adj, std_log_results.rsquared_adj]
                best_R2_adj_id = np.argmax(R2s_adj)

                if best_R2_id == 0:
                    std_var_diff = std_lin_results.params[1] * (max(std_exog) - min(std_exog))
                else:
                    y2 = np.exp(std_lin_results.params[1] * max(std_exog) + std_lin_results.params[0])
                    y1 = np.exp(std_lin_results.params[1] * min(std_exog) + std_lin_results.params[0])
                    std_var_diff = y2 - y1
                std_var_diff = abs(std_var_diff)

                config.metrics['item'].append(item)
                aux = self.get_strategy.get_aux(config, item)
                config.metrics['aux'].append(aux)

                config.metrics['gq_f_value'].append(gq_test[0])
                config.metrics['gq_f_p_value'].append(gq_test[1])

                config.metrics['best_type'].append(best_R2_id)
                config.metrics['best_R2'].append(R2s[best_R2_id])
                config.metrics['best_R2_adj'].append(R2s_adj[best_R2_adj_id])
                config.metrics['std_var_diff'].append(std_var_diff)

                config.metrics['std_lin_R2'].append(std_lin_results.rsquared)
                config.metrics['std_lin_R2_adj'].append(std_lin_results.rsquared_adj)
                config.metrics['std_lin_intercept'].append(std_lin_results.params[0])
                config.metrics['std_lin_slope'].append(std_lin_results.params[1])
                config.metrics['std_lin_intercept_std'].append(std_lin_results.bse[0])
                config.metrics['std_lin_slope_std'].append(std_lin_results.bse[1])
                config.metrics['std_lin_intercept_p_value'].append(std_lin_results.pvalues[0])
                config.metrics['std_lin_slope_p_value'].append(std_lin_results.pvalues[1])

                config.metrics['std_log_R2'].append(std_log_results.rsquared)
                config.metrics['std_log_R2_adj'].append(std_log_results.rsquared_adj)
                config.metrics['std_log_intercept'].append(std_log_results.params[0])
                config.metrics['std_log_slope'].append(std_log_results.params[1])
                config.metrics['std_log_intercept_std'].append(std_log_results.bse[0])
                config.metrics['std_log_slope_std'].append(std_log_results.bse[1])
                config.metrics['std_log_intercept_p_value'].append(std_log_results.pvalues[0])
                config.metrics['std_log_slope_p_value'].append(std_log_results.pvalues[1])

    def iterate(self, config, configs_child):
        for item in tqdm(config.base_list, mininterval=60.0, desc=f'{str(config.experiment)} running'):
            if item in config.base_dict:
                self.single(item, config, configs_child)

    def run(self, config, configs_child):
        self.iterate(config, configs_child)


class ClockRunStrategy(RunStrategy):

    def single(self, item, config, configs_child):
        pass

    def iterate(self, config, configs_child):
        pass

    def run(self, config, configs_child):

        if config.experiment.data in [DataType.betas, DataType.betas_adj, DataType.residuals_common, DataType.residuals_special]:

            if config.experiment.method == Method.linreg:

                items = config.experiment_data['items']
                values = config.experiment_data['values']
                test_size = config.experiment_data['test_size']
                train_size = config.experiment_data['train_size']

                target = self.get_strategy.get_target(config)

                type = config.experiment.method_params['type']
                runs = config.experiment.method_params['runs']
                size = min(config.experiment.method_params['size'], train_size, len(items))
                config.experiment.method_params['size'] = size

                if type == ClockExogType.all.value:

                    for exog_id in tqdm(range(0, size), mininterval=60.0, desc=f'clock building'):
                        config.metrics['item'].append(items[exog_id])
                        aux = self.get_strategy.get_aux(config, items[exog_id])
                        config.metrics['aux'].append(aux)

                        clock = Clock(
                            endog_data=target,
                            endog_names=config.attributes.target,
                            exog_data=values[0:exog_id + 1],
                            exog_names=items[0:exog_id + 1],
                            metrics_dict=config.metrics,
                            train_size=train_size,
                            test_size=test_size,
                            exog_num=exog_id + 1,
                            exog_num_comb=exog_id + 1,
                            num_bootstrap_runs=runs
                        )

                        build_clock_linreg(clock)

                elif type == ClockExogType.deep.value:

                    for exog_id in tqdm(range(0, size), mininterval=60.0, desc=f'clock building'):
                        config.metrics['item'].append(exog_id + 1)
                        config.metrics['aux'].append(exog_id + 1)

                        clock = Clock(
                            endog_data=target,
                            endog_names=config.attributes.target,
                            exog_data=values[0:size + 1],
                            exog_names=items[0:size + 1],
                            metrics_dict=config.metrics,
                            train_size=train_size,
                            test_size=test_size,
                            exog_num=size,
                            exog_num_comb=exog_id + 1,
                            num_bootstrap_runs=runs
                        )

                        build_clock_linreg(clock)

                elif type == ClockExogType.single.value:

                    config.metrics['item'].append(size)
                    config.metrics['aux'].append(size)

                    clock = Clock(
                        endog_data=target,
                        endog_names=config.attributes.target,
                        exog_data=values[0:size],
                        exog_names=items[0:size],
                        metrics_dict=config.metrics,
                        train_size=train_size,
                        test_size=test_size,
                        exog_num=size,
                        exog_num_comb=size,
                        num_bootstrap_runs=runs
                    )

                    build_clock_linreg(clock)


class PlotRunStrategy(RunStrategy):

    def single(self, item, config_child, configs_child):
        pass

    def iterate(self, config, configs_child):
        pass

    def run(self, config, configs_child):

        if config.experiment.data in [DataType.betas, DataType.betas_adj, DataType.residuals_common, DataType.residuals_special]:

            if config.experiment.method == Method.scatter:

                item = config.experiment.method_params['item']
                details = config.experiment.method_params['details']
                std_semi_window = config.experiment.method_params['std_semi_window']

                plot_data = []

                for config_child in configs_child:

                    curr_plot_data = []

                    targets = self.get_strategy.get_target(config_child)
                    methylation = self.get_strategy.get_single_base(config_child, [item])[0]
                    color = cl.scales['8']['qual']['Set1'][configs_child.index(config_child)]
                    coordinates = color[4:-1].split(',')
                    color_transparent = 'rgba(' + ','.join(coordinates) + ',' + str(0.1) + ')'
                    color_border = 'rgba(' + ','.join(coordinates) + ',' + str(0.8) + ')'

                    scatter = go.Scatter(
                        x=targets,
                        y=methylation,
                        name=get_names(config_child),
                        mode='markers',
                        marker=dict(
                            size=4,
                            color=color_border,
                            line=dict(
                                width=1,
                                color=color_border,
                            )
                        ),
                    )
                    curr_plot_data.append(scatter)

                    if config_child.experiment.method == Method.linreg:

                        x = sm.add_constant(targets)
                        y = methylation

                        results = sm.OLS(y, x).fit()

                        intercept = results.params[0]
                        slope = results.params[1]
                        intercept_std = results.bse[0]
                        slope_std = results.bse[1]

                        if std_semi_window != 'none':
                            residuals = results.resid
                            std_x, std_y = residuals_variance(targets, residuals, std_semi_window)

                            std_y_t = np.zeros(len(std_y), dtype=float)
                            std_y_b = np.zeros(len(std_y), dtype=float)
                            for std_id in range(0, len(std_x)):
                                std_y_t[std_id] = (slope * std_x[std_id] + intercept) + std_y[std_id]
                                std_y_b[std_id] = (slope * std_x[std_id] + intercept) - std_y[std_id]

                            scatter = go.Scatter(
                                x=std_x,
                                y=std_y_t,
                                name=get_names(config_child),
                                mode='lines',
                                line=dict(
                                    width=4,
                                    color=color_border
                                ),
                                showlegend=False
                            )
                            curr_plot_data.append(scatter)

                            scatter = go.Scatter(
                                x=std_x,
                                y=std_y_b,
                                name=get_names(config_child),
                                mode='lines',
                                line=dict(
                                    width=4,
                                    color=color_border
                                ),
                                showlegend=False
                            )
                            curr_plot_data.append(scatter)

                        # Adding regression line
                        if details >= 1:
                            x_min = np.min(targets)
                            x_max = np.max(targets)
                            y_min = slope * x_min + intercept
                            y_max = slope * x_max + intercept
                            scatter = go.Scatter(
                                x=[x_min, x_max],
                                y=[y_min, y_max],
                                mode='lines',
                                marker=dict(
                                    color=color
                                ),
                                line=dict(
                                    width=6,
                                    color=color
                                ),
                                showlegend=False
                            )

                            curr_plot_data.append(scatter)

                        # Adding polygon area
                        if details >= 2:
                            pr = PolygonRoutines(
                                x=targets,
                                y=[],
                                params={
                                    'intercept': intercept,
                                    'slope': slope,
                                    'intercept_std': intercept_std,
                                    'slope_std': slope_std
                                },
                                method=config_child.experiment.method
                            )
                            scatter = pr.get_scatter(color_transparent)
                            curr_plot_data.append(scatter)

                    elif config_child.experiment.method == Method.variance_linreg:

                        x = sm.add_constant(targets)
                        y = methylation

                        results = sm.OLS(y, x).fit()
                        intercept = results.params[0]
                        slope = results.params[1]

                        residuals = results.resid
                        diffs = np.abs(residuals)
                        results_var = sm.OLS(diffs, x).fit()

                        intercept_var = results_var.params[0]
                        slope_var = results_var.params[1]

                        # Adding regression line
                        if details >= 1:
                            x_min = np.min(targets)
                            x_max = np.max(targets)
                            y_min = slope * x_min + intercept
                            y_max = slope * x_max + intercept
                            scatter = go.Scatter(
                                x=[x_min, x_max],
                                y=[y_min, y_max],
                                mode='lines',
                                marker=dict(
                                    color=color,
                                ),
                                line=dict(
                                    width=6,
                                    color=color
                                ),
                                showlegend=False
                            )
                            curr_plot_data.append(scatter)

                        # Adding polygon area
                        if details >= 1:
                            pr = PolygonRoutines(
                                x=targets,
                                y=[],
                                params={
                                    'intercept': intercept,
                                    'slope': slope,
                                    'intercept_var': intercept_var,
                                    'slope_var': slope_var,
                                },
                                method=config_child.experiment.method
                            )
                            scatter = pr.get_scatter(color)
                            curr_plot_data.append(scatter)

                    plot_data += curr_plot_data

                config.experiment_data['data'] = plot_data

            elif config.experiment.method == Method.variance_histogram:

                item = config.experiment.method_params['item']

                plot_data = {
                    'hist_data': [],
                    'group_labels': [],
                    'colors': []
                }

                for config_child in configs_child:

                    plot_data['group_labels'].append(str(config_child.attributes.observables))
                    plot_data['colors'].append(cl.scales['8']['qual']['Set1'][configs_child.index(config_child)])

                    targets = self.get_strategy.get_target(config_child)
                    methylation = self.get_strategy.get_single_base(config_child, [item])[0]

                    if config_child.experiment.method == Method.linreg:
                        x = sm.add_constant(targets)
                        y = methylation

                        results = sm.OLS(y, x).fit()

                        plot_data['hist_data'].append(results.resid)

                config.experiment_data['data'] = plot_data

            elif config.experiment.method == Method.curve:

                x_target = config.experiment.method_params['x']
                y_target = config.experiment.method_params['y']
                number_of_points = int(config.experiment.method_params['number_of_points'])

                plot_data = []

                for config_child in configs_child:

                    if x_target == 'count':
                        xs = list(range(1, number_of_points + 1))
                    else:
                        if x_target in config_child.advanced_data:
                            xs = config_child.advanced_data[x_target][0:number_of_points]
                        else:
                            raise ValueError(f'{x_target} not in {config_child}.')

                    if y_target in config_child.advanced_data:
                        ys = config_child.advanced_data[y_target][0:number_of_points]
                    else:
                        raise ValueError(f'{y_target} not in {config_child}.')

                    color = cl.scales['8']['qual']['Set1'][configs_child.index(config_child)]
                    coordinates = color[4:-1].split(',')
                    color_transparent = 'rgba(' + ','.join(coordinates) + ',' + str(0.5) + ')'
                    color_border = 'rgba(' + ','.join(coordinates) + ',' + str(0.9) + ')'

                    scatter = go.Scatter(
                        x=xs,
                        y=ys,
                        name=get_names(config_child),
                        mode='lines+markers',
                        marker=dict(
                            size=10,
                            color=color_transparent,
                            line=dict(
                                width=2,
                                color=color_border,
                            )
                        ),
                    )
                    plot_data.append(scatter)

                config.experiment_data['data'] = plot_data

        elif config.experiment.data == DataType.epimutations:

            if config.experiment.method == Method.scatter:

                plot_data = []

                y_type = config.experiment.method_params['y_type']

                for config_child in configs_child:

                    indexes = config_child.attributes_indexes

                    x = self.get_strategy.get_target(config_child)
                    y = np.zeros(len(indexes), dtype=int)

                    for subj_id in range(0, len(indexes)):
                        subj_col = self.get_strategy.get_single_base(config_child, [subj_id])
                        y[subj_id] = np.sum(subj_col)

                    color = cl.scales['8']['qual']['Set1'][configs_child.index(config_child)]
                    coordinates = color[4:-1].split(',')
                    color_transparent = 'rgba(' + ','.join(coordinates) + ',' + str(0.7) + ')'
                    color_border = 'rgba(' + ','.join(coordinates) + ',' + str(0.8) + ')'

                    scatter = go.Scatter(
                        x=x,
                        y=y,
                        name=get_names(config_child),
                        mode='markers',
                        marker=dict(
                            size=4,
                            color=color_transparent,
                            line=dict(
                                width=1,
                                color=color_border,
                            )
                        ),
                    )
                    plot_data.append(scatter)

                    # Adding regression line

                    x_linreg = sm.add_constant(x)
                    if y_type == 'log':
                        y_linreg = np.log(y)
                    else:
                        y_linreg = y

                    results = sm.OLS(y_linreg, x_linreg).fit()

                    intercept = results.params[0]
                    slope = results.params[1]

                    x_min = np.min(x)
                    x_max = np.max(x)
                    if y_type == 'log':
                        y_min = np.exp(slope * x_min + intercept)
                        y_max = np.exp(slope * x_max + intercept)
                    else:
                        y_min = slope * x_min + intercept
                        y_max = slope * x_max + intercept
                    scatter = go.Scatter(
                        x=[x_min, x_max],
                        y=[y_min, y_max],
                        mode='lines',
                        marker=dict(
                            color=color
                        ),
                        line=dict(
                            width=6,
                            color=color
                        ),
                        showlegend=False
                    )

                    plot_data.append(scatter)

                config.experiment_data['data'] = plot_data

            elif config.experiment.method == Method.range:

                plot_data = []

                borders = config.experiment.method_params['borders']

                for config_child in configs_child:

                    color = cl.scales['8']['qual']['Set1'][configs_child.index(config_child)]
                    coordinates = color[4:-1].split(',')
                    color_transparent = 'rgba(' + ','.join(coordinates) + ',' + str(0.5) + ')'

                    indexes = config_child.attributes_indexes

                    x = self.get_strategy.get_target(config_child)
                    y = np.zeros(len(indexes), dtype=int)

                    for subj_id in range(0, len(indexes)):
                        subj_col = self.get_strategy.get_single_base(config_child, [subj_id])
                        y[subj_id] = np.sum(subj_col)

                    for seg_id in range(0, len(borders) - 1):
                        x_center = (borders[seg_id + 1] + borders[seg_id]) * 0.5
                        curr_box = []
                        for subj_id in range(0, len(indexes)):
                            if borders[seg_id] <= x[subj_id] < borders[seg_id + 1]:
                                curr_box.append(y[subj_id])

                        trace = go.Box(
                            y=curr_box,
                            x=[x_center] * len(curr_box),
                            name=f'{borders[seg_id]} to {borders[seg_id + 1] - 1}',
                            marker=dict(
                                color=color_transparent
                            )
                        )
                        plot_data.append(trace)

                config.experiment_data['data'] = plot_data

        elif config.experiment.data == DataType.entropy:

            if config.experiment.method == Method.scatter:

                plot_data = []

                for config_child in configs_child:

                    indexes = config_child.attributes_indexes

                    x = self.get_strategy.get_target(config_child)
                    y = self.get_strategy.get_single_base(config_child, indexes)

                    color = cl.scales['8']['qual']['Set1'][configs_child.index(config_child)]
                    coordinates = color[4:-1].split(',')
                    color_transparent = 'rgba(' + ','.join(coordinates) + ',' + str(0.7) + ')'
                    color_border = 'rgba(' + ','.join(coordinates) + ',' + str(0.8) + ')'

                    scatter = go.Scatter(
                        x=x,
                        y=y,
                        name=get_names(config_child),
                        mode='markers',
                        marker=dict(
                            size=4,
                            color=color_transparent,
                            line=dict(
                                width=1,
                                color=color_border,
                            )
                        ),
                    )
                    plot_data.append(scatter)

                    # Adding regression line

                    x_linreg = sm.add_constant(x)
                    y_linreg = y

                    results = sm.OLS(y_linreg, x_linreg).fit()

                    intercept = results.params[0]
                    slope = results.params[1]

                    x_min = np.min(x)
                    x_max = np.max(x)
                    y_min = slope * x_min + intercept
                    y_max = slope * x_max + intercept
                    scatter = go.Scatter(
                        x=[x_min, x_max],
                        y=[y_min, y_max],
                        mode='lines',
                        marker=dict(
                            color=color
                        ),
                        line=dict(
                            width=6,
                            color=color
                        ),
                        showlegend=False
                    )

                    plot_data.append(scatter)

                config.experiment_data['data'] = plot_data

        elif config.experiment.data == DataType.observables:

            if config.experiment.method == Method.histogram:

                plot_data = []
                for config_child in configs_child:

                    curr_plot_data = []

                    targets = self.get_strategy.get_target(config_child)
                    is_number_list = [is_float(t) for t in targets]
                    if False in is_number_list:
                        xbins = {}
                    else:
                        bin_size = config.experiment.method_params['bin_size']
                        xbins = dict(
                            start=min(targets) - 0.5 * bin_size,
                            end=max(targets) + 0.5 * bin_size,
                            size=bin_size
                        )

                    color = cl.scales['8']['qual']['Set1'][configs_child.index(config_child)]

                    if config_child.experiment.method == Method.histogram:
                        histogram = go.Histogram(
                            x=targets,
                            name=get_names(config_child),
                            xbins=xbins,
                            marker=dict(
                                opacity=config.experiment.method_params['opacity'],
                                color=color,
                                line=dict(
                                    color='#444444',
                                    width=1
                                )
                            )
                        )

                        curr_plot_data.append(histogram)

                    plot_data += curr_plot_data

                config.experiment_data['data'] = plot_data
