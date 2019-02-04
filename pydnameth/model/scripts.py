from anytree import Node
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.config.experiment.types import Task, Method
from pydnameth.config.config import Config
from pydnameth.model.tree import calc_tree


def proc_table_linreg(
    data,
    annotations,
    attributes
):
    config_root = Config(
        data=data,
        experiment=Experiment(
            task=Task.table,
            method=Method.linreg,
            params={}
        ),
        annotations=annotations,
        attributes=attributes
    )

    root = Node(name=str(config_root), config=config_root)
    calc_tree(root)
    
def proc_table_linreg_var(
    data,
    annotations,
    attributes
):
    pass

def proc_table_polygon(
    data,
    annotations,
    attributes,
    clear_run=False
):
    pass

def proc_clock_linreg(
    data,
    annotations,
    attributes
):
    pass

def plot_observables_histogram(
    data,
    annotations,
    attributes,
    clear_run=False
):
    pass

def plot_methylation_scatter(
    data,
    annotations,
    attributes
):
    pass



