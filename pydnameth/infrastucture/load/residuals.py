from pydnameth.infrastucture.path import get_data_base_path
from pydnameth.infrastucture.load.cpg import load_cpg
import numpy as np
import os.path
import pickle
import pandas as pd
from statsmodels import api as sm


def load_residuals(config):
    suffix = 'cells(' + str(config.attributes.cells) + ')'

    fn_dict = get_data_base_path(config) + '/' + 'residuals_dict_' + suffix + '.pkl'
    fn_data = get_data_base_path(config) + '/' + 'residuals_' + suffix + '.npz'

    if os.path.isfile(fn_dict) and os.path.isfile(fn_data):

        f = open(fn_dict, 'rb')
        config.residuals_dict = pickle.load(f)
        f.close()

        data = np.load(fn_data)
        config.residuals_data = data['residuals_data']

    else:

        load_cpg(config)

        config.residuals_dict = config.cpg_dict
        f = open(fn_dict, 'wb')
        pickle.dump(config.residuals_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()

        exog_df = pd.DataFrame(config.cells_dict)

        num_cpgs = len(config.cpg_dict.keys())
        num_subjects = len(config.cpg_data[np.ix_([0], config.attributes_indexes)][0])
        config.residuals_data = np.zeros((num_cpgs, num_subjects), dtype=np.float32)

        for cpg, row in config.cpg_dict.items():
            betas = config.cpg_data[np.ix_([row], config.attributes_indexes)][0]

            endog_dict = {cpg: betas}
            endog_df = pd.DataFrame(endog_dict)

            reg_res = sm.OLS(endog=endog_df, exog=exog_df).fit()

            residuals = reg_res.resid

            config.residuals_data[row] = list(map(np.float32, residuals))

        np.savez_compressed(fn_data, residuals_data=config.residuals_data)
