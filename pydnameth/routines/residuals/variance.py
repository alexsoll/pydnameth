import numpy as np
import statsmodels.api as sm


def process_box(targets, values, semi_window=2, box_b='left', box_t='right'):
    targets = np.squeeze(np.asarray(targets))
    values = np.squeeze(np.asarray(values))

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
        curr_residuals = values[point_id]
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
        q5, q1, median, q3, q95 = np.percentile(np.asarray(curr_residuals), [5, 25, 50, 75, 95])
        iqr = q3 - q1
        ms[x_id] = median
        if box_b == 'left':
            bs[x_id] = q1 - 1.5 * iqr
        elif box_b == 'Q1':
            bs[x_id] = q1
        elif box_b == 'Q5':
            bs[x_id] = q5
        else:
            raise ValueError('Unknown box_b type')

        if box_t == 'right':
            ts[x_id] = q3 + 1.5 * iqr
        elif box_t == 'Q3':
            ts[x_id] = q3
        elif box_t == 'Q95':
            ts[x_id] = q95
        else:
            raise ValueError('Unknown box_t type')

    return xs, bs, ms, ts


def variance_processing(exog, endog, characteristics_dict, key_prefix):
    is_same_elements = all(x == endog[0] for x in endog)
    if is_same_elements:
        characteristics_dict[key_prefix + '_lin_lin_R2'].append(1.0)
        characteristics_dict[key_prefix + '_lin_lin_intercept'].append(0.0)
        characteristics_dict[key_prefix + '_lin_lin_slope'].append(0.0)
        characteristics_dict[key_prefix + '_lin_lin_intercept_std'].append(0.0)
        characteristics_dict[key_prefix + '_lin_lin_slope_std'].append(0.0)
        characteristics_dict[key_prefix + '_lin_lin_intercept_p_value'].append('NA')
        characteristics_dict[key_prefix + '_lin_lin_slope_p_value'].append('NA')
        R2s = [1.0]
    else:
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

    if 'best_type' not in characteristics_dict:
        characteristics_dict['best_type'] = []
    if 'best_R2' not in characteristics_dict:
        characteristics_dict['best_R2'] = []
