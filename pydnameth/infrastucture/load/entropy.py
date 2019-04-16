from pydnameth.infrastucture.load.betas import load_betas
from pydnameth.infrastucture.load.betas_adj import load_betas_adj
from pydnameth.infrastucture.load.residuals_common import load_residuals_common
from pydnameth.infrastucture.path import get_cache_path
import numpy as np
import copy
import os.path
from tqdm import tqdm


def load_entropy(config):
    suffix = ''
    if bool(config.experiment.data_params):
        data_params = copy.deepcopy(config.experiment.data_params)
        suffix += '_' + config.experiment.get_data_params_str()
    else:
        raise ValueError(f'Exog for entropy is empty.')

    fn_data = get_cache_path(config) + '/' + 'entropy' + suffix + '.npz'

    if os.path.isfile(fn_data):

        data = np.load(fn_data)
        config.entropy_data = data['data']

    else:

        if data_params['data'] == 'betas':
            config.experiment.data_params = {}
            load_betas(config)
            data = config.betas_data
            data_dict = config.betas_dict
        elif data_params['data'] == 'betas_adj':
            config.experiment.data_params.pop('data')
            load_betas_adj(config)
            data = config.betas_adj_data
            data_dict = config.betas_adj_dict
        elif data_params['data'] == 'residuals_common':
            config.experiment.data_params.pop('data')
            load_residuals_common(config)
            data = config.residuals_data
            data_dict = config.residuals_dict
        else:
            raise ValueError(f'Unsupported data for entropy.')

        num_subjects = data.shape[1]
        config.entropy_data = np.zeros(num_subjects, dtype=np.float32)

        rows = [data_dict[item] for item in config.cpg_list if item in data_dict]

        for subj_id in tqdm(range(0, num_subjects), mininterval=60.0, desc='residuals_data creating'):
            values = np.squeeze(np.asarray(data[np.ix_(rows, [subj_id])]))
            entropy = 0.0
            outliers = 0
            for val in values:
                if 0.0 < val < 1.0:
                    entropy += val * np.log2(val) + (1.0 - val) * np.log2(1.0 - val)
                else:
                    outliers += 1
            entropy /= ((len(values) - outliers) * np.log2(0.5))
            config.entropy_data[subj_id] = entropy

        np.savez_compressed(fn_data, data=config.entropy_data)

        # Clear data
        del data
