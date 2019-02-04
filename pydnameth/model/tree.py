from anytree import PostOrderIter, PreOrderIter
from pydnameth.infrastucture.save.info import save_info
from pydnameth.model.context import Context
import hashlib
import copy
import json

def calc_tree(root):

    for node in PreOrderIter(root):
        node_json = json.dumps(node.name, sort_keys=True).encode("utf-8")
        hash = hashlib.md5(node_json).hexdigest()
        node.config.set_hash(hash)
        save_info(node)

    for node in PostOrderIter(root):
        config = node.config
        configs_child = [node_child.config for node_child in node.children]
        context = Context(config)
        context.pipeline(config, configs_child)
