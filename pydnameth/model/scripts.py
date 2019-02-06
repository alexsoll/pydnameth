from anytree import Node
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.config.experiment.types import DataType, Task, Method
from pydnameth.config.config import Config
from pydnameth.model.tree import calc_tree
from pydnameth.config.attributes.attributes import Attributes, Observables, Cells


def cpg_proc_table_linreg(
    data,
    annotations,
    attributes
):
    config_root = Config(
        data=data,
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=Method.linreg,
            params={}
        ),
        annotations=annotations,
        attributes=attributes
    )

    root = Node(name=str(config_root), config=config_root)
    calc_tree(root)
    
def cpg_proc_table_variance_linreg(
    data,
    annotations,
    attributes
):
    config_root = Config(
        data=data,
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=Method.variance_linreg,
            params={}
        ),
        annotations=annotations,
        attributes=attributes
    )

    root = Node(name=str(config_root), config=config_root)
    calc_tree(root)

def cpg_proc_table_polygon(
    data,
    annotations,
    attributes,
    observables_list,
    child_method = Method.linreg
):
    config_root = Config(
        data=data,
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=Method.polygon,
            params={}
        ),
        annotations=annotations,
        attributes=attributes
    )
    root = Node(name=str(config_root), config=config_root)

    for d in observables_list:

        observables_child = Observables(
            name=attributes.observables.name,
            types=d
        )

        cells_child = Cells(
            name=attributes.cells.name,
            types=attributes.cells.types
        )

        attributes_child = Attributes(
            target=attributes.target,
            observables=observables_child,
            cells=cells_child,
        )

        config_child = Config(
            data=data,
            experiment=Experiment(
                type=DataType.cpg,
                task=Task.table,
                method=child_method,
                params={}
            ),
            annotations=annotations,
            attributes=attributes_child
        )
        Node(name=str(config_child), config=config_child, parent=root)

    calc_tree(root)

def cpg_proc_table_z_test_linreg(
    data,
    annotations,
    attributes,
    observables_list,
    child_method = Method.linreg
):
    config_root = Config(
        data=data,
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=Method.z_test_linreg,
            params={}
        ),
        annotations=annotations,
        attributes=attributes
    )
    root = Node(name=str(config_root), config=config_root)

    for d in observables_list:

        observables_child = Observables(
            name=attributes.observables.name,
            types=d
        )

        cells_child = Cells(
            name=attributes.cells.name,
            types=attributes.cells.types
        )

        attributes_child = Attributes(
            target=attributes.target,
            observables=observables_child,
            cells=cells_child,
        )

        config_child = Config(
            data=data,
            experiment=Experiment(
                type=DataType.cpg,
                task=Task.table,
                method=child_method,
                params={}
            ),
            annotations=annotations,
            attributes=attributes_child
        )
        Node(name=str(config_child), config=config_child, parent=root)

    calc_tree(root)

def cpg_proc_clock_linreg(
    data,
    annotations,
    attributes,
    child_method = Method.linreg
):
    config_root = Config(
        data=data,
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.clock,
            method=Method.linreg,
            params={}
        ),
        annotations=annotations,
        attributes=attributes
    )
    root = Node(name=str(config_root), config=config_root)

    config_child = Config(
        data=data,
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=child_method,
            params={}
        ),
        annotations=annotations,
        attributes=attributes
    )

    Node(name=str(config_child), config=config_child, parent=root)

    calc_tree(root)

def cpg_plot_methylation_scatter(
    data,
    annotations,
    attributes,
    cpg_list,
    observables_list,
    child_method=Method.linreg,
):
    for cpg in cpg_list:

        config_root = Config(
            data=data,
            experiment=Experiment(
                type=DataType.cpg,
                task=Task.methylation,
                method=Method.scatter,
                params={}
            ),
            annotations=annotations,
            attributes=attributes
        )
        config_root.experiment.params['item'] = cpg

        root = Node(name=str(config_root), config=config_root)

        for d in observables_list:
            observables_child = Observables(
                name=attributes.observables.name,
                types=d
            )

            cells_child = Cells(
                name=attributes.cells.name,
                types=attributes.cells.types
            )

            attributes_child = Attributes(
                target=attributes.target,
                observables=observables_child,
                cells=cells_child,
            )

            config_child = Config(
                data=data,
                experiment=Experiment(
                    type=DataType.cpg,
                    task=Task.table,
                    method=child_method,
                    params={}
                ),
                annotations=annotations,
                attributes=attributes_child,
                is_run=False
            )
            Node(name=str(config_child), config=config_child, parent=root)

        calc_tree(root)


def attributes_plot_observables_histogram(
    data,
    annotations,
    attributes,
    observables_list,
):
    config_root = Config(
        data=data,
        experiment=Experiment(
            type=DataType.attributes,
            task=Task.observables,
            method=Method.histogram,
            params={}
        ),
        annotations=annotations,
        attributes=attributes
    )
    root = Node(name=str(config_root), config=config_root)

    for d in observables_list:
        observables_child = Observables(
            name=attributes.observables.name,
            types=d
        )

        cells_child = Cells(
            name=attributes.cells.name,
            types=attributes.cells.types
        )

        attributes_child = Attributes(
            target=attributes.target,
            observables=observables_child,
            cells=cells_child,
        )

        config_child = Config(
            data=data,
            experiment=config_root.experiment,
            annotations=annotations,
            attributes=attributes_child,
            is_run=False
        )
        Node(name=str(config_child), config=config_child, parent=root)

    calc_tree(root)





