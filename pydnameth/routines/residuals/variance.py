import numpy as np
import statsmodels.api as sm


def residuals_std(targets, residuals, semi_window=2):
    targets = np.squeeze(np.asarray(targets))
    residuals = np.squeeze(np.asarray(residuals))

    min_target = int(np.floor(min(targets)))
    max_target = int(np.ceil(max(targets)))
    window_residuals = {}
    window_targets = {}
    for center in range(min_target, max_target + 1):
        window_residuals[center] = []
        window_targets[center] = []

    for point_id in range(0, len(targets)):
        curr_target = targets[point_id]
        curr_target_round = int(round(curr_target))
        curr_residuals = residuals[point_id]
        for window_id in range(curr_target_round - semi_window, curr_target_round + semi_window + 1):
            if window_id in window_residuals:
                window_residuals[window_id].append(curr_residuals)
                window_targets[window_id].append(curr_target)

    xs = list(window_targets.keys())
    ys = np.zeros(len(xs), dtype=float)
    for x_id in range(0, len(xs)):
        curr_residuals = window_residuals[xs[x_id]]
        ys[x_id] = np.std(curr_residuals)

    return xs, ys


def residuals_box(targets, residuals, semi_window=2):
    targets = np.squeeze(np.asarray(targets))
    residuals = np.squeeze(np.asarray(residuals))

    min_target = int(np.floor(min(targets)))
    max_target = int(np.ceil(max(targets)))
    window_residuals = {}
    window_targets = {}
    for center in range(min_target, max_target + 1):
        window_residuals[center] = []
        window_targets[center] = []

    for point_id in range(0, len(targets)):
        curr_target = targets[point_id]
        curr_target_round = int(round(curr_target))
        curr_residuals = residuals[point_id]
        for window_id in range(curr_target_round - semi_window, curr_target_round + semi_window + 1):
            if window_id in window_residuals:
                window_residuals[window_id].append(curr_residuals)
                window_targets[window_id].append(curr_target)

    xs = list(window_targets.keys())
    bs = np.zeros(len(xs), dtype=float)
    ms = np.zeros(len(xs), dtype=float)
    ts = np.zeros(len(xs), dtype=float)
    for x_id in range(0, len(xs)):
        curr_residuals = window_residuals[xs[x_id]]
        q1, median, q3 = np.percentile(np.asarray(curr_residuals), [25, 50, 75])
        iqr = q3 - q1
        bs[x_id] = q1 - 1.5 * iqr
        ms[x_id] = median
        ts[x_id] = q3 + 1.5 * iqr

    return xs, bs, ms, ts


def variance_processing(exog, endog, characteristics_dict, key_prefix):
    lin_exog = sm.add_constant(exog)
    lin_endog = endog
    lin_results = sm.OLS(lin_endog, lin_exog).fit()

    characteristics_dict[key_prefix + '_lin_R2'].append(lin_results.rsquared)
    characteristics_dict[key_prefix + '_lin_intercept'].append(lin_results.params[0])
    characteristics_dict[key_prefix + '_lin_slope'].append(lin_results.params[1])
    characteristics_dict[key_prefix + '_lin_intercept_std'].append(lin_results.bse[0])
    characteristics_dict[key_prefix + '_lin_slope_std'].append(lin_results.bse[1])
    characteristics_dict[key_prefix + '_lin_intercept_p_value'].append(lin_results.pvalues[0])
    characteristics_dict[key_prefix + '_lin_slope_p_value'].append(lin_results.pvalues[1])

    if min(endog) > 0:
        log_exog = sm.add_constant(exog)
        log_endog = np.log(endog)
        log_results = sm.OLS(log_endog, log_exog).fit()

        characteristics_dict[key_prefix + '_log_R2'].append(log_results.rsquared)
        characteristics_dict[key_prefix + '_log_intercept'].append(log_results.params[0])
        characteristics_dict[key_prefix + '_log_slope'].append(log_results.params[1])
        characteristics_dict[key_prefix + '_log_intercept_std'].append(log_results.bse[0])
        characteristics_dict[key_prefix + '_log_slope_std'].append(log_results.bse[1])
        characteristics_dict[key_prefix + '_log_intercept_p_value'].append(log_results.pvalues[0])
        characteristics_dict[key_prefix + '_log_slope_p_value'].append(log_results.pvalues[1])

        R2s = [lin_results.rsquared, log_results.rsquared]
        best_R2_id = np.argmax(R2s)
        best_R2 = R2s[best_R2_id]
    else:
        characteristics_dict[key_prefix + '_log_R2'].append('NA')
        characteristics_dict[key_prefix + '_log_intercept'].append('NA')
        characteristics_dict[key_prefix + '_log_slope'].append('NA')
        characteristics_dict[key_prefix + '_log_intercept_std'].append('NA')
        characteristics_dict[key_prefix + '_log_slope_std'].append('NA')
        characteristics_dict[key_prefix + '_log_intercept_p_value'].append('NA')
        characteristics_dict[key_prefix + '_log_slope_p_value'].append('NA')

        best_R2_id = 0
        best_R2 = lin_results.rsquared

    characteristics_dict[key_prefix + '_best_type'].append(best_R2_id)
    characteristics_dict[key_prefix + '_best_R2'].append(best_R2)




