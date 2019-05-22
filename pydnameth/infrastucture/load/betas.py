from pydnameth.infrastucture.path import get_data_base_path
import numpy as np
import os.path
import pickle
from tqdm import tqdm


def get_line_list(line):
    line_list = line.split('\t')
    for val_id in range(0, len(line_list)):
        line_list[val_id] = line_list[val_id].replace('"', '').rstrip()
    return line_list


def load_betas(config):
    fn_dict = get_data_base_path(config) + '/' + 'betas_dict.pkl'

    suffix = ''
    if bool(config.experiment.data_params):
        suffix += '_' + str(config.experiment.get_data_params_str())

    fn_data = get_data_base_path(config) + '/' + 'betas' + suffix
    fn_txt = fn_data + '.txt'
    fn_npz = fn_data + '.npz'

    if os.path.isfile(fn_dict) and os.path.isfile(fn_npz):

        f = open(fn_dict, 'rb')
        config.betas_dict = pickle.load(f)
        f.close()

        data = np.load(fn_npz)
        config.betas_data = data['data']

    else:

        config.betas_dict = {}

        f = open(fn_txt)
        f.readline()
        cpg_id = 0
        for line in tqdm(f, mininterval=60.0, desc='betas_dict creating'):
            line_list = get_line_list(line)
            cpg = line_list[0]

            if 'NA' in line_list:
                raise ValueError(f'{cpg} contains NA')

            else:
                config.betas_dict[cpg] = cpg_id
                cpg_id += 1

        f.close()

        f = open(fn_dict, 'wb')
        pickle.dump(config.betas_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()

        num_cpgs = cpg_id

        f = open(fn_txt)
        header_line = f.readline()
        headers = header_line.split('\t')
        headers = [x.rstrip() for x in headers]
        subjects = headers[1:len(headers)]

        config.betas_data = np.zeros((num_cpgs, len(subjects)), dtype=np.float32)

        cpg_id = 0
        for line in tqdm(f, mininterval=60.0, desc='betas_data creating'):
            line_list = get_line_list(line)
            curr_data = list(map(np.float32, line_list[1::]))
            config.betas_data[cpg_id] = curr_data
            cpg_id += 1

        f.close()

        np.savez_compressed(fn_npz, data=config.betas_data)
