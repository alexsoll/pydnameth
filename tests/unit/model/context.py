import unittest
from tests.definitions import ROOT_DIR
from pydnameth import Data
from pydnameth import Experiment
from pydnameth import Annotations
from pydnameth import Observables
from pydnameth import Cells
from pydnameth import Attributes
from pydnameth import Config
from pydnameth.model.context import Context
from pydnameth.model.strategy.load import CPGLoadStrategy
from pydnameth.model.strategy.load import AttributesLoadStrategy
from pydnameth.model.strategy.get import CPGGetStrategy
from pydnameth.model.strategy.get import AttributesGetStrategy
from pydnameth.model.strategy.setup import TableSetUpStrategy
from pydnameth.model.strategy.setup import ClockSetUpStrategy
from pydnameth.model.strategy.setup import MethylationSetUpStrategy
from pydnameth.model.strategy.setup import ObservablesSetUpStrategy
from pydnameth.model.strategy.proc import TableRunStrategy
from pydnameth.model.strategy.proc import ClockRunStrategy
from pydnameth.model.strategy.proc import MethylationRunStrategy
from pydnameth.model.strategy.proc import ObservablesRunStrategy
from pydnameth.model.strategy.release import TableReleaseStrategy
from pydnameth.model.strategy.release import ClockReleaseStrategy
from pydnameth.model.strategy.release import MethylationReleaseStrategy
from pydnameth.model.strategy.release import ObservablesReleaseStrategy
from pydnameth.model.strategy.save import TableSaveStrategy
from pydnameth.model.strategy.save import ClockSaveStrategy
from pydnameth.model.strategy.save import MethylationSaveStrategy
from pydnameth.model.strategy.save import ObservablesSaveStrategy
from pydnameth.config.experiment.types import Task
from pydnameth.config.experiment.types import DataType


class TestAnnotationsConditions(unittest.TestCase):
    def setUp(self):
        data = Data(
            name='cpg_beta',
            path=ROOT_DIR,
            base='fixtures'
        )

        annotations = Annotations(
            name='annotations',
            exclude='excluded',
            cross_reactive='ex',
            snp='ex',
            chr='NS',
            gene_region='yes',
            geo='any',
            probe_class='A_B'
        )

        observables = Observables(
            name='observables',
            types={}
        )

        cells = Cells(
            name='cells',
            types='any'
        )

        attributes = Attributes(
            target='age',
            observables=observables,
            cells=cells
        )

        self.config = Config(
            data=data,
            experiment=None,
            annotations=annotations,
            attributes=attributes,
            is_run=True,
            is_root=True
        )

    def check_strategy(self, data_type, task, needed_list):
        experiment = Experiment(type=data_type, task=task, method=None, params=None)
        self.config.experiment = experiment
        context = Context(self.config)
        condition = True

        real_list = ['load_strategy', 'get_strategy', 'setup_strategy',
                     'run_strategy', 'release_strategy', 'save_strategy']
        real_list = [getattr(context, x) for x in real_list]
        for real, needed in zip(real_list, needed_list):
            if type(real) != needed:
                condition = False
                break

        return condition

    def test_strategy_creation_cpg_table(self):
        condition = self.check_strategy(DataType.cpg, Task.table,
                                        [CPGLoadStrategy, CPGGetStrategy, TableSetUpStrategy,
                                         TableRunStrategy, TableReleaseStrategy, TableSaveStrategy])
        self.assertEqual(condition, True)

    def test_strategy_creation_attr_table(self):
        condition = self.check_strategy(DataType.attributes, Task.table,
                                        [AttributesLoadStrategy, AttributesGetStrategy, TableSetUpStrategy,
                                         TableRunStrategy, TableReleaseStrategy, TableSaveStrategy])
        self.assertEqual(condition, True)

    def test_strategy_creation_cpg_clock(self):
        condition = self.check_strategy(DataType.cpg, Task.clock,
                                        [CPGLoadStrategy, CPGGetStrategy, ClockSetUpStrategy,
                                         ClockRunStrategy, ClockReleaseStrategy, ClockSaveStrategy])
        self.assertEqual(condition, True)

    def test_strategy_creation_attr_clock(self):
        condition = self.check_strategy(DataType.attributes, Task.clock,
                                        [AttributesLoadStrategy, AttributesGetStrategy, ClockSetUpStrategy,
                                         ClockRunStrategy, ClockReleaseStrategy, ClockSaveStrategy])
        self.assertEqual(condition, True)

    def test_strategy_creation_cpg_methylation(self):
        condition = self.check_strategy(DataType.cpg, Task.methylation,
                                        [CPGLoadStrategy, CPGGetStrategy, MethylationSetUpStrategy,
                                         MethylationRunStrategy, MethylationReleaseStrategy, MethylationSaveStrategy])
        self.assertEqual(condition, True)

    def test_strategy_creation_attr_methylation(self):
        condition = self.check_strategy(DataType.attributes, Task.methylation,
                                        [AttributesLoadStrategy, AttributesGetStrategy, MethylationSetUpStrategy,
                                         MethylationRunStrategy, MethylationReleaseStrategy, MethylationSaveStrategy])
        self.assertEqual(condition, True)

    def test_strategy_creation_cpg_observables(self):
        condition = self.check_strategy(DataType.cpg, Task.observables,
                                        [CPGLoadStrategy, CPGGetStrategy, ObservablesSetUpStrategy,
                                         ObservablesRunStrategy, ObservablesReleaseStrategy, ObservablesSaveStrategy])
        self.assertEqual(condition, True)

    def test_strategy_creation_attr_observables(self):
        condition = self.check_strategy(DataType.attributes, Task.observables,
                                        [AttributesLoadStrategy, AttributesGetStrategy, ObservablesSetUpStrategy,
                                         ObservablesRunStrategy, ObservablesReleaseStrategy, ObservablesSaveStrategy])
        self.assertEqual(condition, True)