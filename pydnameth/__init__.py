# -*- coding: utf-8 -*-

"""Top-level package for pydnameth."""
# flake8: noqa

__author__ = """Aaron Blare"""
__email__ = 'aaron.blare@mail.ru'
__version__ = '0.2.3'

from .config.config import Config
from .config.common import CommonTypes
from .config.annotations.annotations import Annotations
from .config.annotations.types import AnnotationKey
from .config.annotations.types import Exclude, CrossReactive, SNP, Chromosome, GeneRegion, Geo, ProbeClass
from .config.attributes.attributes import Cells, Observables, Attributes
from .config.data.data import Data
from .config.data.types import DataPath, DataBase
from .config.experiment.experiment import Experiment
from .config.experiment.types import DataType, Task, Method

from pydnameth.scripts.develop.betas.table import \
    betas_table_aggregator_dev,\
    betas_table_aggregator_var_dev,\
    betas_table_linreg_dev,\
    betas_table_cluster_dev,\
    betas_table_polygon_dev,\
    betas_table_variance_linreg_dev,\
    betas_table_z_test_linreg_dev
from pydnameth.scripts.develop.betas.clock import \
    betas_clock_linreg_dev,\
    betas_special_clock_linreg_dev
from pydnameth.scripts.develop.betas.plot import \
    betas_plot_scatter_dev,\
    betas_clock_plot_curve_dev,\
    betas_plot_scatter_var_dev,\
    betas_plot_variance_histogram_dev

from pydnameth.scripts.develop.epimutations.load import \
    epimutations_load_dev
from pydnameth.scripts.develop.epimutations.plot import \
    epimutations_plot_scatter_dev,\
    epimutations_plot_range_dev

from pydnameth.scripts.develop.entropy.plot import \
    entropy_plot_scatter_dev

from pydnameth.scripts.develop.observables.plot import \
    observables_plot_histogram_dev

from pydnameth.scripts.develop.residuals_common.plot import \
    residuals_common_plot_scatter_dev
from pydnameth.scripts.develop.residuals_common.table import \
    residuals_common_table_aggregator_dev,\
    residuals_common_table_linreg_dev, \
    residuals_common_table_heteroscedasticity_dev,\
    residuals_common_table_aggregator_variance

from pydnameth.scripts.develop.residuals_special.plot import \
    residuals_special_plot_scatter_dev
from pydnameth.scripts.develop.residuals_special.table import \
    residuals_special_table_aggregator_dev,\
    residuals_special_table_linreg_dev

from pydnameth.scripts.release.betas.clock import \
    betas_clock_linreg
from pydnameth.scripts.release.betas.plot import \
    cpg_plot_methylation_scatter
from pydnameth.scripts.release.betas.table import \
    cpg_proc_table_linreg,\
    cpg_proc_table_polygon,\
    cpg_proc_table_z_test_linreg

from pydnameth.scripts.release.observables.plot import \
    observables_plot_histogram

