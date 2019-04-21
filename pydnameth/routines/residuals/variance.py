import numpy as np


def residuals_variance(targets, residuals, semi_window=2):
    targets = np.squeeze(np.asarray(targets))
    residuals = np.squeeze(np.asarray(residuals))

    min_target = int(np.floor(min(targets)))
    max_target = int(np.ceil(max(targets)))
    window_residuals = {}
    window_targets = {}
    for center in range(min_target + semi_window, max_target - semi_window + 1):
        window_residuals[center] = []
        window_targets[center] = []

    for point_id in range(0, len(targets)):
        curr_target = targets[point_id]
        curr_target_round = int(round(curr_target))
        curr_resid = residuals[point_id]
        for window_id in range(curr_target_round - semi_window, curr_target_round + semi_window + 1):
            if window_id in window_residuals:
                window_residuals[window_id].append(curr_resid)
                window_targets[window_id].append(curr_target)

    xs = list(window_targets.keys())
    ys = np.zeros(len(xs), dtype=float)
    for x_id in range(0, len(xs)):
        curr_resid = window_residuals[xs[x_id]]
        ys[x_id] = np.std(curr_resid)

    return xs, ys
