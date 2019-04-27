import copy
import os
from shutil import copyfile
from anytree import Node
from pydnameth.config.config import Config
from pydnameth.config.experiment.types import Task, Method, DataType
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.infrastucture.file_name import get_file_name
from pydnameth.infrastucture.path import get_save_path
from pydnameth.model.tree import build_tree, calc_tree


def betas_clock_linreg(
    data,
    annotations,
    attributes,
    method_params=None
):
    config_root = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            data=DataType.betas,
            task=Task.clock,
            method=Method.linreg,
            method_params=copy.deepcopy(method_params)
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
            data=DataType.betas,
            task=Task.table,
            method=Method.linreg
        ),
        annotations=copy.deepcopy(annotations),
        attributes=copy.deepcopy(attributes),
        is_run=True,
        is_root=False
    )

    Node(name=str(config_child), config=config_child, parent=root)

    build_tree(root)
    calc_tree(root)


def betas_clock_special(
    data,
    annotations,
    attributes,
    file,
    method_params=None,
):
    """
        Producing epigentic clock, using best CpGs which are provided in input file.

        Epigentic clock represents as table:
        Each row corresponds to clocks, which are built on all CpGs from the previous rows including the current row.
        Columns:

        * item: CpG id.
        * aux: gene, on which CpG is mapped.
        * R2: determination coefficient of linear regression between real and predicted target observable.
          A statistical measure of how well the regression line approximates the data points.
        * r: correlation coefficient of linear regression between real and predicted target observable.
        * evs: explained variance regression score.
        * mae: mean absolute error regression loss.
        * rmse: root mean square error

        Possible parameters of experiment:

        * ``'type'``: type of clocks. \n
          Possible options: \n
          ``'all'``: iterative building of clocks starting from one element in the model,
          ending with ``'size'`` elements in the model. \n
          ``'single '``: building of clocks only with ``'size'`` elements in the model. \n
          ``'deep'``: iterative building of clocks starting from one element in the model,
          ending with ``'size'`` elements in the model, but choosing all possible combinations from ``'size'`` elements.
        * ``'part'``: the proportion of considered number of subject in the test set. From ``0.0`` to ``1.0``.
        * ``'size'``: maximum number of exogenous variables in a model.
        * ``'runs'`` number of bootstrap runs in model

        :param data: pdm.Data instance, which specifies information about dataset.
        :param annotations: pdm.Annotations instance, which specifies subset of CpGs.
        :param attributes: pdm.Attributes instance, which specifies information about subjects.
        :param method_params: parameters of experiment.
     """

    if os.path.isfile(file):

        head, tail = os.path.split(file)
        fn = os.path.splitext(tail)[0]
        ext = os.path.splitext(tail)[1]

        config_root = Config(
            data=copy.deepcopy(data),
            experiment=Experiment(
                data=DataType.betas,
                task=Task.clock,
                method=Method.linreg,
                method_params=copy.deepcopy(method_params)
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
                data=DataType.betas,
                task=Task.table,
                method=Method.special,
                method_params={'file_name': fn}
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
