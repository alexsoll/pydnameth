from anytree import PostOrderIter, PreOrderIter
from pydnameth.infrastucture.save.info import save_info
from pydnameth.model.context import Context
import hashlib
import jsonpickle
import copy


def calc_tree(root):

    for node in PostOrderIter(root):
        config = copy.deepcopy(node.config)
        hide_node(node)
        node_json = jsonpickle.encode(node).encode('utf-8')
        node.config = config
        hash = hashlib.md5(node_json).hexdigest()
        node.config.set_hash(hash)
        save_info(node)

    for node in PostOrderIter(root):
        config = node.config
        configs_child = [node_child.config for node_child in node.children]
        context = Context(config)
        context.pipeline(config, configs_child)


def hide_node(node):
    node.config.experiment.params = {}
    node.config.data.path = ''
    node.config.data.name = ''
    node.config.annotations.name = ''
    node.config.attributes.observables.name = ''
    node.config.attributes.cells.name = ''
