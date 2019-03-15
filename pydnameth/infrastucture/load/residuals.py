from pydnameth.infrastucture.load.cpg import load_cpg
import numpy as np
import pandas as pd
from statsmodels import api as sm


def load_residuals(config):

    load_cpg(config)

    config.residuals_dict = config.cpg_dict

    exog_df = pd.DataFrame(config.cells_dict)

    num_cpgs = len(config.cpg_dict.keys())
    num_subjects = len(config.cpg_data[np.ix_([0], config.attributes_indexes)][0])
    config.residuals_data = np.zeros((num_cpgs, num_subjects), dtype=np.float32)

    for cpg, row in config.cpg_dict.items():
        betas = config.cpg_data[np.ix_([row], config.attributes_indexes)][0]

        endog_dict = {cpg: betas}
        endog_df = pd.DataFrame(endog_dict)

        reg_res = sm.OLS(endog=endog_df, exog=exog_df).fit()

        residuals = list(map(np.float32, reg_res.resid))
        config.residuals_data[row] = residuals

    # Clear cpg_data
    config.cpg_data = np.zeros(0)
