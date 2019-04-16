import copy
from anytree import Node
from pydnameth.config.config import Config
from pydnameth.config.experiment.types import Task, Method
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.config.attributes.attributes import Observables, Cells, Attributes
from pydnameth.model.tree import build_tree, calc_tree


def plot_scatter_dev(
    data_type,
    data,
    annotations,
    attributes,
    cpg_list,
    observables_list,
    child_method=Method.linreg,
    method_params=None
):
    for cpg in cpg_list:

        config_root = Config(
            data=copy.deepcopy(data),
            experiment=Experiment(
                data=data_type,
                task=Task.plot,
                method=Method.scatter,
                method_params=copy.deepcopy(method_params)
            ),
            annotations=copy.deepcopy(annotations),
            attributes=copy.deepcopy(attributes),
            is_run=True,
            is_root=True
        )

        if config_root.experiment.method_params is None:
            config_root.experiment.method_params = dict()

        config_root.experiment.method_params['item'] = cpg

        root = Node(name=str(config_root), config=config_root)

        for d in observables_list:
            observables_child = Observables(
                name=copy.deepcopy(attributes.observables.name),
                types=d
            )

            cells_child = Cells(
                name=copy.deepcopy(attributes.cells.name),
                types=copy.deepcopy(attributes.cells.types)
            )

            attributes_child = Attributes(
                target=copy.deepcopy(attributes.target),
                observables=observables_child,
                cells=cells_child,
            )

            config_child = Config(
                data=copy.deepcopy(data),
                experiment=Experiment(
                    data=data_type,
                    task=Task.table,
                    method=copy.deepcopy(child_method)
                ),
                annotations=copy.deepcopy(annotations),
                attributes=attributes_child,
                is_run=False,
                is_root=False
            )
            Node(name=str(config_child), config=config_child, parent=root)

        build_tree(root)
        calc_tree(root)
