from pydnameth.infrastucture.path import get_data_base_path
import numpy as np
import os.path
import pickle
from tqdm import tqdm

from pydnameth.infrastucture.load.betas import get_line_list


def load_genes(config):
    fn_dict = get_data_base_path(config) + '/' + 'bops_dict.pkl'
    suffix = ''

    if bool(config.experiment.data_params):
        suffix += '_' + str(config.experiment.get_data_params_str())

    fn_betas_txt = get_data_base_path(config) + '/' + 'betas' + suffix + '.txt'
    fn_bops_npz = get_data_base_path(config) + '/' + 'bops' + suffix + '.npz'

    if os.path.isfile(fn_dict) and os.path.isfile(fn_bops_npz):
        f = open(fn_dict, 'rb')

        config.bop_dict = pickle.load(f)
        f.close()
        data = np.load(fn_bops_npz)
        config.bop_dict = data['data']
    else:
        config.bop_dict = {}
        config.bop_list = []
        for bop_id, bop in enumerate(config.bop_cpg_dict):
            config.gene_dict[bop] = bop_id
            config.gene_list.append(bop)

        f = open(fn_dict, 'wb')
        pickle.dump(config.bop_dict, f, pickle.HIGHEST_PROTOCOL)
        f.close()
        f = open(fn_betas_txt)
        header_line = f.readline()
        headers = header_line.split('\t')
        headers = [x.rstrip() for x in headers]
        subjects = headers[1:len(headers)]

        config.bop_data = np.zeros((len(config.bop_list), len(subjects)), dtype=np.float32)

        bop_id = 0

        for line in tqdm(f, mininterval=60.0, desc='gene_data creating'):
            line_list = get_line_list(line)
            curr_cpg_name = line_list[0]
            curr_data = list(map(np.float32, line_list[1::]))
            for bop in config.cpg_bop_dict[curr_cpg_name]:
                line_num = config.gene_dict[bop]
                config.bop_data[line_num] += curr_data

            bop_id += 1
        f.close()

        for row_id, row in enumerate(config.bop_data):
            config.bop_data[row_id] /= len(config.bop_cpg_dict[config.bop_list[row_id]])

        np.savez_compressed(fn_bops_npz, data=config.bop_data)
