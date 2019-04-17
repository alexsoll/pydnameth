from pydnameth.infrastucture.load.betas import load_betas
from pydnameth.infrastucture.path import get_data_base_path
from pydnameth.infrastucture.load.attributes import load_cells_dict, load_observables_dict
import numpy as np
import pandas as pd
from statsmodels import api as sm
import pickle
import os.path
from tqdm import tqdm


def load_residuals_common(config):

    fn_dict = get_data_base_path(config) + '/' + 'residuals_common_dict.pkl'

    suffix = ''
    if bool(config.experiment.data_params):
        data_params = config.experiment.data_params
        suffix += '_' + config.experiment.get_data_params_str()
    else:
        raise ValueError(f'Exog for residuals is empty.')

    fn_data = get_data_base_path(config) + '/' + 'residuals_common' + suffix + '.npz'

    if os.path.isfile(fn_dict) and os.path.isfile(fn_data):

        f = open(fn_dict, 'rb')
        config.residuals_dict = pickle.load(f)
        f.close()

        data = np.load(fn_data)
        config.residuals_data = data['data']

    else:

        config.experiment.data_params = {}
        load_betas(config)

        config.residuals_dict = config.betas_dict
        f = open(fn_dict, 'wb')
        pickle.dump(config.residuals_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()

        config.residuals_dict = config.betas_dict

        exog_dict = {}

        if 'cells' in data_params:

            cells_dict = load_cells_dict(config)

            if isinstance(data_params['cells'], list):
                all_types = list(cells_dict.keys())
                for key in all_types:
                    if key not in data_params['cells']:
                        cells_dict.pop(key)

                if len(list(cells_dict.keys())) != len(data_params['cells']):
                    raise ValueError(f'Wrong number of cells types.')

                exog_dict.update(cells_dict)

        if 'observables' in data_params:

            observables_dict = load_observables_dict(config)
            if isinstance(data_params['observables'], list):
                all_types = list(observables_dict.keys())
                for key in all_types:
                    if key not in data_params['observables']:
                        observables_dict.pop(key)

                if len(list(observables_dict.keys())) != len(data_params['observables']):
                    raise ValueError(f'Wrong number of observables types.')

                exog_dict.update(observables_dict)

        exog_df = pd.DataFrame(exog_dict)

        num_cpgs = config.betas_data.shape[0]
        num_subjects = config.betas_data.shape[1]
        config.residuals_data = np.zeros((num_cpgs, num_subjects), dtype=np.float32)

        for cpg, row in tqdm(config.betas_dict.items(), mininterval=60.0, desc='residuals_data creating'):
            betas = config.betas_data[row, :]

            endog_dict = {cpg: betas}
            endog_df = pd.DataFrame(endog_dict)

            reg_res = sm.OLS(endog=endog_df, exog=exog_df).fit()

            residuals = list(map(np.float32, reg_res.resid))
            config.residuals_data[row] = residuals

        np.savez_compressed(fn_data, data=config.residuals_data)

        # Clear data
        del config.betas_data
