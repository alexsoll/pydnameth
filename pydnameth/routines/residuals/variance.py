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


def residuals_box(targets, residuals, semi_window=2, box_b='left', box_t='right'):
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
        ms[x_id] = median
        if box_b == 'left':
            bs[x_id] = q1 - 1.5 * iqr
        elif box_b == 'Q1':
            bs[x_id] = q1
        else:
            raise ValueError('Unknown box_b type')

        if box_t == 'right':
            ts[x_id] = q3 + 1.5 * iqr
        elif box_t == 'Q3':
            ts[x_id] = q3
        else:
            raise ValueError('Unknown box_t type')

    return xs, bs, ms, ts


def variance_processing(exog, endog, characteristics_dict, key_prefix):
    lin_lin_exog = sm.add_constant(exog)
    lin_lin_endog = endog
    lin_lin_results = sm.OLS(lin_lin_endog, lin_lin_exog).fit()
    characteristics_dict[key_prefix + '_lin_lin_R2'].append(lin_lin_results.rsquared)
    characteristics_dict[key_prefix + '_lin_lin_intercept'].append(lin_lin_results.params[0])
    characteristics_dict[key_prefix + '_lin_lin_slope'].append(lin_lin_results.params[1])
    characteristics_dict[key_prefix + '_lin_lin_intercept_std'].append(lin_lin_results.bse[0])
    characteristics_dict[key_prefix + '_lin_lin_slope_std'].append(lin_lin_results.bse[1])
    characteristics_dict[key_prefix + '_lin_lin_intercept_p_value'].append(lin_lin_results.pvalues[0])
    characteristics_dict[key_prefix + '_lin_lin_slope_p_value'].append(lin_lin_results.pvalues[1])
    R2s = [lin_lin_results.rsquared]

    if min(endog) > 0:
        lin_log_exog = sm.add_constant(exog)
        lin_log_endog = np.log(endog)
        lin_log_results = sm.OLS(lin_log_endog, lin_log_exog).fit()
        characteristics_dict[key_prefix + '_lin_log_R2'].append(lin_log_results.rsquared)
        characteristics_dict[key_prefix + '_lin_log_intercept'].append(lin_log_results.params[0])
        characteristics_dict[key_prefix + '_lin_log_slope'].append(lin_log_results.params[1])
        characteristics_dict[key_prefix + '_lin_log_intercept_std'].append(lin_log_results.bse[0])
        characteristics_dict[key_prefix + '_lin_log_slope_std'].append(lin_log_results.bse[1])
        characteristics_dict[key_prefix + '_lin_log_intercept_p_value'].append(lin_log_results.pvalues[0])
        characteristics_dict[key_prefix + '_lin_log_slope_p_value'].append(lin_log_results.pvalues[1])
        R2s.append(lin_log_results.rsquared)

    else:
        characteristics_dict[key_prefix + '_lin_log_R2'].append('NA')
        characteristics_dict[key_prefix + '_lin_log_intercept'].append('NA')
        characteristics_dict[key_prefix + '_lin_log_slope'].append('NA')
        characteristics_dict[key_prefix + '_lin_log_intercept_std'].append('NA')
        characteristics_dict[key_prefix + '_lin_log_slope_std'].append('NA')
        characteristics_dict[key_prefix + '_lin_log_intercept_p_value'].append('NA')
        characteristics_dict[key_prefix + '_lin_log_slope_p_value'].append('NA')
        R2s.append(-1)

    if min(endog) > 0 and min(exog) > 0:
        log_log_exog = sm.add_constant(np.log(exog))
        log_log_endog = np.log(endog)
        log_log_results = sm.OLS(log_log_endog, log_log_exog).fit()
        characteristics_dict[key_prefix + '_log_log_R2'].append(log_log_results.rsquared)
        characteristics_dict[key_prefix + '_log_log_intercept'].append(log_log_results.params[0])
        characteristics_dict[key_prefix + '_log_log_slope'].append(log_log_results.params[1])
        characteristics_dict[key_prefix + '_log_log_intercept_std'].append(log_log_results.bse[0])
        characteristics_dict[key_prefix + '_log_log_slope_std'].append(log_log_results.bse[1])
        characteristics_dict[key_prefix + '_log_log_intercept_p_value'].append(log_log_results.pvalues[0])
        characteristics_dict[key_prefix + '_log_log_slope_p_value'].append(log_log_results.pvalues[1])
        R2s.append(log_log_results.rsquared)

    else:
        characteristics_dict[key_prefix + '_log_log_R2'].append('NA')
        characteristics_dict[key_prefix + '_log_log_intercept'].append('NA')
        characteristics_dict[key_prefix + '_log_log_slope'].append('NA')
        characteristics_dict[key_prefix + '_log_log_intercept_std'].append('NA')
        characteristics_dict[key_prefix + '_log_log_slope_std'].append('NA')
        characteristics_dict[key_prefix + '_log_log_intercept_p_value'].append('NA')
        characteristics_dict[key_prefix + '_log_log_slope_p_value'].append('NA')
        R2s.append(-1)

    best_R2_id = np.argmax(R2s)
    best_R2 = R2s[best_R2_id]

    characteristics_dict[key_prefix + '_best_type'].append(best_R2_id)
    characteristics_dict[key_prefix + '_best_R2'].append(best_R2)


def init_variance_characteristics_dict(characteristics_dict, key_prefix):
    characteristics_dict[key_prefix + '_lin_lin_R2'] = []
    characteristics_dict[key_prefix + '_lin_lin_intercept'] = []
    characteristics_dict[key_prefix + '_lin_lin_slope'] = []
    characteristics_dict[key_prefix + '_lin_lin_intercept_std'] = []
    characteristics_dict[key_prefix + '_lin_lin_slope_std'] = []
    characteristics_dict[key_prefix + '_lin_lin_intercept_p_value'] = []
    characteristics_dict[key_prefix + '_lin_lin_slope_p_value'] = []
    characteristics_dict[key_prefix + '_lin_log_R2'] = []
    characteristics_dict[key_prefix + '_lin_log_intercept'] = []
    characteristics_dict[key_prefix + '_lin_log_slope'] = []
    characteristics_dict[key_prefix + '_lin_log_intercept_std'] = []
    characteristics_dict[key_prefix + '_lin_log_slope_std'] = []
    characteristics_dict[key_prefix + '_lin_log_intercept_p_value'] = []
    characteristics_dict[key_prefix + '_lin_log_slope_p_value'] = []
    characteristics_dict[key_prefix + '_log_log_R2'] = []
    characteristics_dict[key_prefix + '_log_log_intercept'] = []
    characteristics_dict[key_prefix + '_log_log_slope'] = []
    characteristics_dict[key_prefix + '_log_log_intercept_std'] = []
    characteristics_dict[key_prefix + '_log_log_slope_std'] = []
    characteristics_dict[key_prefix + '_log_log_intercept_p_value'] = []
    characteristics_dict[key_prefix + '_log_log_slope_p_value'] = []
    characteristics_dict[key_prefix + '_best_type'] = []
    characteristics_dict[key_prefix + '_best_R2'] = []
    characteristics_dict['best_type'] = []
    characteristics_dict['best_R2'] = []
