from pydnameth.infrastucture.load.cpg import load_cpg
from pydnameth.infrastucture.path import get_data_base_path
import numpy as np
import pickle
import os.path
from tqdm import tqdm
from pydnameth.infrastucture.save.table import save_table_dict_csv


def load_epimutations(config):
    fn_dict = get_data_base_path(config) + '/' + 'epimutations_dict'

    suffix = ''
    if bool(config.experiment.data_params):
        suffix += '_' + str(config.experiment.get_data_params_str())

    fn_data = get_data_base_path(config) + '/' + 'epimutations' + suffix

    if os.path.isfile(fn_dict + '.pkl') and os.path.isfile(fn_data + '.npz'):

        f = open(fn_dict + '.pkl', 'rb')
        config.epimutations_dict = pickle.load(f)
        f.close()

        data = np.load(fn_data + '.npz')
        config.epimutations_data = data['data']

    else:

        config.experiment.data_params = {}
        load_cpg(config)

        config.epimutations_dict = config.betas_dict
        f = open(fn_dict + '.pkl', 'wb')
        pickle.dump(config.epimutations_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()

        save_table_dict_csv(
            fn_dict,
            {
                'item': list(config.epimutations_dict.keys()),
                'row': list(config.epimutations_dict.values())
            }
        )

        num_cpgs = config.betas_data.shape[0]
        num_subjects = config.betas_data.shape[1]
        config.epimutations_data = np.zeros((num_cpgs, num_subjects), dtype=np.int)

        for cpg, row in tqdm(config.betas_dict.items(), mininterval=60.0):
            betas = config.betas_data[row, :]
            quartiles = np.percentile(betas, [25, 75])
            iqr = quartiles[1] - quartiles[0]
            left = quartiles[0] - (3.0 * iqr)
            right = quartiles[1] + (3.0 * iqr)

            curr_row = np.zeros(num_subjects, dtype=np.int)
            for subject_id in range(0, num_subjects):
                curr_point = betas[subject_id]
                if curr_point < left or curr_point > right:
                    curr_row[subject_id] = 1

            config.epimutations_data[row] = curr_row

        np.savez_compressed(fn_data + '.npz', data=config.epimutations_data)
        np.savetxt(fn_data + '.txt', config.epimutations_data, delimiter='\t', fmt='%d')

        # Clear cpg_data
        del config.betas_data
