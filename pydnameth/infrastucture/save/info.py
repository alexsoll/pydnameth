from pydnameth.infrastucture.path import get_experiment_path
from anytree import RenderTree
import os


def save_info(root):
    fn = get_experiment_path(root.config) + '/info.txt'
    fr = open(fn, 'r')
    lines = fr.read().splitlines()
    fr.close()
    if str(root.config.hash) not in lines:
        fa = open(fn, 'a')
        for pre, _, node in RenderTree(root):
            fa.write(root.config.hash + '\n')
            fa.write(f'{pre}{node.name}')
            fa.write('\n\n')
        fa.close()
