from anytree import Node
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.config.annotations.annotations import Annotations
from pydnameth.config.experiment.types import DataType, Task, Method
from pydnameth.config.config import Config
from pydnameth.model.tree import build_tree, calc_tree
from pydnameth.config.attributes.attributes import Attributes, Observables, Cells
from pydnameth.infrastucture.path import get_save_path
from pydnameth.infrastucture.file_name import get_file_name
from pydnameth.infrastucture.load.epimutations import load_epimutations
import copy
from shutil import copyfile
import os


def load_epimutations_dev(data):

    config = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.epimutations,
            task=None,
            method=None,
            params=None
        ),
        annotations=Annotations(
            name='annotations',
            exclude='bad_cpgs',
            cross_reactive='any',
            snp='any',
            chr='NS',
            gene_region='any',
            geo='any',
            probe_class='any'
        ),
        attributes=Attributes(
            target=None,
            observables=None,
            cells=None
        ),
        is_run=True,
        is_root=True
    )

    load_epimutations(config)


def cpg_proc_table_linreg_dev(
    data,
    annotations,
    attributes,
    params=None
):
    proc_table_linreg(
        DataType.cpg,
        data,
        annotations,
        attributes,
        params
    )


def residuals_common_proc_table_linreg_dev(
    data,
    annotations,
    attributes,
    params=None
):
    proc_table_linreg(
        DataType.residuals_common,
        data,
        annotations,
        attributes,
        params
    )


def residuals_special_proc_table_linreg_dev(
    data,
    annotations,
    attributes,
    params=None
):
    proc_table_linreg(
        DataType.residuals_special,
        data,
        annotations,
        attributes,
        params
    )


def proc_table_linreg(
    data_type,
    data,
    annotations,
    attributes,
    params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=data_type,
            task=Task.table,
            method=Method.linreg,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
    )

    root = Node(name=str(config_root), config=config_root)
    build_tree(root)
    calc_tree(root)


def cpg_proc_table_variance_linreg_dev(
    data,
    annotations,
    attributes,
    params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=Method.variance_linreg,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
    )

    root = Node(name=str(config_root), config=config_root)
    build_tree(root)
    calc_tree(root)


def cpg_proc_table_polygon_dev(
    data,
    annotations,
    attributes,
    observables_list,
    child_method=Method.linreg,
    params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=Method.polygon,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
    )
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
                type=DataType.cpg,
                task=Task.table,
                method=copy.deepcopy(child_method),
                params={}
            ),
            annotations=copy.deepcopy(annotations),
            attributes=attributes_child,
            is_run=True,
            is_root=False
        )
        Node(name=str(config_child), config=config_child, parent=root)

    build_tree(root)
    calc_tree(root)


def cpg_proc_table_z_test_linreg_dev(
    data,
    annotations,
    attributes,
    observables_list,
    child_method=Method.linreg,
    params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=Method.z_test_linreg,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
    )
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
                type=DataType.cpg,
                task=Task.table,
                method=copy.deepcopy(child_method),
                params={}
            ),
            annotations=copy.deepcopy(annotations),
            attributes=attributes_child,
            is_run=True,
            is_root=False
        )
        Node(name=str(config_child), config=config_child, parent=root)

    build_tree(root)
    calc_tree(root)


def cpg_proc_table_aggregator_dev(
    data,
    annotations,
    attributes,
    observables_list,
    params=None
):
    proc_table_aggregator(
        DataType.cpg,
        data,
        annotations,
        attributes,
        observables_list,
        params
    )


def cpg_proc_table_aggregator_var_dev(
    data,
    annotations,
    attributes,
    observables_list,
    params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=Method.aggregator,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
    )
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
                type=DataType.cpg,
                task=Task.table,
                method=copy.deepcopy(Method.variance_linreg),
                params={}
            ),
            annotations=copy.deepcopy(annotations),
            attributes=attributes_child,
            is_run=True,
            is_root=False
        )
        Node(name=str(config_child), config=config_child, parent=root)

    observables_cluster = Observables(
        name=copy.deepcopy(attributes.observables.name),
        types={}
    )

    cells_cluster = Cells(
        name=copy.deepcopy(attributes.cells.name),
        types=copy.deepcopy(attributes.cells.types)
    )

    attributes_cluster = Attributes(
        target=copy.deepcopy(attributes.target),
        observables=observables_cluster,
        cells=cells_cluster,
    )

    config_cluster = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=copy.deepcopy(Method.cluster),
            params={}
        ),
        annotations=copy.deepcopy(annotations),
        attributes=attributes_cluster,
        is_run=True,
        is_root=False
    )
    Node(name=str(config_cluster), config=config_cluster, parent=root)

    build_tree(root)
    calc_tree(root)


def residuals_common_proc_table_aggregator_dev(
    data,
    annotations,
    attributes,
    observables_list,
    params=None
):
    proc_table_aggregator(
        DataType.residuals_common,
        data,
        annotations,
        attributes,
        observables_list,
        params
    )


def residuals_special_proc_table_aggregator_dev(
    data,
    annotations,
    attributes,
    observables_list,
    params=None
):
    proc_table_aggregator(
        DataType.residuals_special,
        data,
        annotations,
        attributes,
        observables_list,
        params
    )


def proc_table_aggregator(
    data_type,
    data,
    annotations,
    attributes,
    observables_list,
    params=None
):
    child_methods_lvl_1 = [Method.polygon, Method.z_test_linreg]
    child_methods_lvl_2 = [Method.linreg]

    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=data_type,
            task=Task.table,
            method=Method.aggregator,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
    )
    root = Node(name=str(config_root), config=config_root)

    for child_method_lvl_1 in child_methods_lvl_1:
        config_lvl_1 = Config(
            data=copy.deepcopy(data),
            experiment=Experiment(
                type=data_type,
                task=Task.table,
                method=child_method_lvl_1,
                params={}
            ),
            annotations=copy.deepcopy(annotations),
            attributes=copy.deepcopy(attributes),
            is_run=True,
            is_root=False
        )
        node_lvl_1 = Node(name=str(config_lvl_1), config=config_lvl_1, parent=root)

        for child_method_lvl_2 in child_methods_lvl_2:
            for d in observables_list:
                observables_lvl_2 = Observables(
                    name=copy.deepcopy(attributes.observables.name),
                    types=d
                )

                cells_lvl_2 = Cells(
                    name=copy.deepcopy(attributes.cells.name),
                    types=copy.deepcopy(attributes.cells.types)
                )

                attributes_lvl_2 = Attributes(
                    target=copy.deepcopy(attributes.target),
                    observables=observables_lvl_2,
                    cells=cells_lvl_2,
                )

                config_lvl_2 = Config(
                    data=copy.deepcopy(data),
                    experiment=Experiment(
                        type=data_type,
                        task=Task.table,
                        method=copy.deepcopy(child_method_lvl_2),
                        params={}
                    ),
                    annotations=copy.deepcopy(annotations),
                    attributes=attributes_lvl_2,
                    is_run=True,
                    is_root=False
                )
                Node(name=str(config_lvl_2), config=config_lvl_2, parent=node_lvl_1)

    build_tree(root)
    calc_tree(root)


def cpg_proc_clock_linreg_dev(
    data,
    annotations,
    attributes,
    child_method=Method.linreg,
    params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.clock,
            method=Method.linreg,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
    )
    root = Node(name=str(config_root), config=config_root)

    config_child = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.cpg,
            task=Task.table,
            method=copy.deepcopy(child_method),
            params={}
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=False
    )

    Node(name=str(config_child), config=config_child, parent=root)

    build_tree(root)
    calc_tree(root)


def cpg_proc_special_clock_linreg_dev(
    data,
    annotations,
    attributes,
    file,
    params=None,
):
    if os.path.isfile(file):

        head, tail = os.path.split(file)
        fn = os.path.splitext(tail)[0]
        ext = os.path.splitext(tail)[1]

        config_root = Config(
            data=copy.deepcopy(data),
            experiment=Experiment(
                type=DataType.cpg,
                task=Task.clock,
                method=Method.linreg,
                params=copy.deepcopy(params)
            ),
            annotations=copy.deepcopy(annotations),
            attributes=copy.deepcopy(attributes),
            is_run=True,
            is_root=True
        )
        root = Node(name=str(config_root), config=config_root)

        config_child = Config(
            data=copy.deepcopy(data),
            experiment=Experiment(
                type=DataType.cpg,
                task=Task.table,
                method=Method.special,
                params={'file_name': fn}
            ),
            annotations=copy.deepcopy(annotations),
            attributes=copy.deepcopy(attributes),
            is_run=False,
            is_root=False
        )

        Node(name=str(config_child), config=config_child, parent=root)

        build_tree(root)

        new_file = get_save_path(config_child) + '/' + \
            get_file_name(config_child) + ext

        copyfile(file, new_file)

        calc_tree(root)

    else:
        raise FileNotFoundError(f'File {file} not found.')


def plot_methylation_scatter_dev(
    data_type,
    data,
    annotations,
    attributes,
    cpg_list,
    observables_list,
    child_method=Method.linreg,
    params=None
):
    for cpg in cpg_list:

        config_root = Config(
            data=copy.deepcopy(data),
            experiment=Experiment(
                type=data_type,
                task=Task.methylation,
                method=Method.scatter,
                params=copy.deepcopy(params)
            ),
            annotations=copy.deepcopy(annotations),
            attributes=copy.deepcopy(attributes),
            is_run=True,
            is_root=True
        )

        if config_root.experiment.params is None:
            config_root.experiment.params = dict()

        config_root.experiment.params['item'] = cpg

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
                    type=data_type,
                    task=Task.table,
                    method=copy.deepcopy(child_method),
                    params={}
                ),
                annotations=copy.deepcopy(annotations),
                attributes=attributes_child,
                is_run=False,
                is_root=False
            )
            Node(name=str(config_child), config=config_child, parent=root)

        build_tree(root)
        calc_tree(root)


def cpg_plot_methylation_scatter_dev(
    data,
    annotations,
    attributes,
    cpg_list,
    observables_list,
    child_method=Method.linreg,
    params=None
):
    plot_methylation_scatter_dev(
        DataType.cpg,
        data,
        annotations,
        attributes,
        cpg_list,
        observables_list,
        child_method,
        params
    )


def cpg_plot_methylation_scatter_var_dev(
    data,
    annotations,
    attributes,
    cpg_list,
    observables_list,
    child_method=Method.variance_linreg,
    params=None
):
    plot_methylation_scatter_dev(
        DataType.cpg,
        data,
        annotations,
        attributes,
        cpg_list,
        observables_list,
        child_method,
        params
    )


def residuals_common_plot_methylation_scatter_dev(
    data,
    annotations,
    attributes,
    cpg_list,
    observables_list,
    child_method=Method.linreg,
    params=None
):
    plot_methylation_scatter_dev(
        DataType.residuals_common,
        data,
        annotations,
        attributes,
        cpg_list,
        observables_list,
        child_method,
        params
    )


def residuals_special_plot_methylation_scatter_dev(
    data,
    annotations,
    attributes,
    cpg_list,
    observables_list,
    child_method=Method.linreg,
    params=None
):
    plot_methylation_scatter_dev(
        DataType.residuals_special,
        data,
        annotations,
        attributes,
        cpg_list,
        observables_list,
        child_method,
        params
    )


def cpg_plot_methylation_variance_histogram_dev(
    data,
    annotations,
    attributes,
    cpg_list,
    observables_list,
    child_method=Method.linreg,
    params=None
):
    for cpg in cpg_list:

        config_root = Config(
            data=copy.deepcopy(data),
            experiment=Experiment(
                type=DataType.cpg,
                task=Task.methylation,
                method=Method.variance_histogram,
                params=copy.deepcopy(params)
            ),
            annotations=copy.deepcopy(annotations),
            attributes=copy.deepcopy(attributes),
            is_run=True,
            is_root=True
        )

        if config_root.experiment.params is None:
            config_root.experiment.params = dict()

        config_root.experiment.params['item'] = cpg

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
                    type=DataType.cpg,
                    task=Task.table,
                    method=copy.deepcopy(child_method),
                    params={}
                ),
                annotations=copy.deepcopy(annotations),
                attributes=attributes_child,
                is_run=False,
                is_root=False
            )
            Node(name=str(config_child), config=config_child, parent=root)

        build_tree(root)
        calc_tree(root)


def attributes_plot_observables_histogram_dev(
    data,
    annotations,
    attributes,
    observables_list,
    params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.attributes,
            task=Task.observables,
            method=Method.histogram,
            params=copy.deepcopy(params)
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=True
    )
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
            experiment=config_root.experiment,
            annotations=copy.deepcopy(annotations),
            attributes=attributes_child,
            is_run=False,
            is_root=True
        )
        Node(name=str(config_child), config=config_child, parent=root)

    build_tree(root)
    calc_tree(root)
