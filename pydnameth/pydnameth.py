# -*- coding: utf-8 -*-

"""Main module."""

from pydnameth.config.config import Config
from pydnameth.config.data.data import Data
from pydnameth.config.setup.setup import Setup
from pydnameth.config.setup.types import Experiment, Task, Method


def get_config(data,
               setup,
               annotations,
               attributes,
               target):
    config = Config(data, setup, annotations, attributes, target)
    return config


def get_data(name,
             type,
             path,
             base):
    data = Data(name, type, path, base)
    return data


def get_setup(experiment,
              task,
              method,
              params):
    if not isinstance(experiment, Experiment):
        raise ValueError('experiment must be Experiment instance')
    if not isinstance(task, Task):
        raise ValueError('task must be Task instance')
    if not isinstance(method, Method):
        raise ValueError('method must be Method instance')

    setup = Setup(experiment, task, method, params)
    return setup
