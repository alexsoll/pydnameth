from pydnameth.infrastucture.load.cpg import load_cpg
from pydnameth.infrastucture.path import get_data_base_path
import copy
import numpy as np
import pickle
import os.path
from tqdm import tqdm
import csv
from pydnameth.infrastucture.save.table import save_table_dict_csv
from joblib import Parallel, delayed


def process_epimutation_row(row, epimutations_data, cpg_data, num_subjects):
    betas = cpg_data[row, :]

    for subject_id in range(0, num_subjects):
        curr_point = betas[subject_id]
        curr_betas = np.delete(betas, subject_id)
        quartiles = np.percentile(curr_betas, [25, 75])
        iqr = quartiles[1] - quartiles[0]
        left = quartiles[0] - (3.0 * iqr)
        right = quartiles[1] + (3.0 * iqr)
        if curr_point < left or curr_point > right:
            epimutations_data[row][subject_id] = 1
        else:
            epimutations_data[row][subject_id] = 0



def load_epimutations(config):
    fn_dict = get_data_base_path(config) + '/' + 'epimutations_dict'
    fn_dict_pkl = fn_dict + '.pkl'
    fn_dict_csv = fn_dict + '.csv'
    fn_data = get_data_base_path(config) + '/' + 'epimutations'
    fn_data_npz = fn_data + '.npz'
    fn_data_csv = fn_data + '.csv'

    if os.path.isfile(fn_dict_pkl) and os.path.isfile(fn_data_npz):

        f = open(fn_dict_pkl, 'rb')
        config.epimutations_dict = pickle.load(f)
        f.close()

        data = np.load(fn_data_npz)
        config.epimutations_data = data['residuals_data']

    else:

        load_cpg(config)

        config.epimutations_dict = config.cpg_dict
        f = open(fn_dict_pkl, 'wb')
        pickle.dump(config.epimutations_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()

        save_table_dict_csv(
            fn_dict,
            {
                'item': list(config.epimutations_dict.keys()),
                'row': list(config.epimutations_dict.values())
            }
        )

        num_cpgs = config.cpg_data.shape[0]
        num_subjects = config.cpg_data.shape[1]
        config.epimutations_data = np.zeros((num_cpgs, num_subjects), dtype=np.int)

        for cpg, row in tqdm(config.cpg_dict.items()):
            betas = config.cpg_data[row, :]

            curr_row = np.zeros(num_subjects, dtype=np.int)

            for subject_id in range(0, num_subjects):
                curr_point = betas[subject_id]
                curr_betas = np.delete(betas, subject_id)
                quartiles = np.percentile(curr_betas, [25, 75])
                iqr = quartiles[1] - quartiles[0]
                left = quartiles[0] - (3.0 * iqr)
                right = quartiles[1] + (3.0 * iqr)
                if curr_point < left or curr_point > right:
                    curr_row[subject_id] = 1

            if 1 in curr_row:
                break

            config.epimutations_data[row] = curr_row

        np.savez_compressed(fn_data_npz, epimutations_data=config.epimutations_data)
        np.savetxt(fn_data_csv, config.epimutations_data, delimiter=",")

        # Clear cpg_data
        del config.cpg_data
