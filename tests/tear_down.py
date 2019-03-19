import os
from pydnameth.infrastucture.path import get_data_base_path


def clear_cache(config):
    path = get_data_base_path(config)
    exts = ('.npz', '.pkl')
    for root, dirs, files in os.walk(path):
        for currentFile in files:
            if currentFile.lower().endswith(exts):
                os.remove(os.path.join(root, currentFile))
