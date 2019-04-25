import unittest
from tests.definitions import ROOT_DIR
from pydnameth import Data
from pydnameth import Experiment
from pydnameth import Annotations
from pydnameth import Observables
from pydnameth import Cells
from pydnameth import Attributes
from pydnameth import Config
from pydnameth.model.strategy.load import BetasLoadStrategy
from pydnameth.model.strategy.get import BetasGetStrategy
from pydnameth.config.experiment.types import Task
from pydnameth.config.experiment.types import DataType
from pydnameth.config.experiment.types import Method
from tests.tear_down import clear_cache


class TestGetStrategy(unittest.TestCase):
    def setUp(self):
        data = Data(
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
            probe_class='any'
        )

        observables = Observables(
            name='observables',
            types={'gender': 'M'}
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

        experiment = Experiment(
            data=DataType.betas,
            task=Task.table,
            method=Method.linreg)

        self.config = Config(
            data=data,
            experiment=experiment,
            annotations=annotations,
            attributes=attributes,
            is_run=True,
            is_root=True
        )

        self.config.initialize()

    def tearDown(self):
        clear_cache(self.config)

    def test_get_strategy_get_target(self):
        load_strategy = BetasLoadStrategy()
        load_strategy.load(self.config, [])

        get_strategy = BetasGetStrategy()
        target = get_strategy.get_target(self.config)

        self.assertEqual(341, len(target))

    def test_betas_get_strategy_single_base_len(self):
        load_strategy = BetasLoadStrategy()
        load_strategy.load(self.config, [])

        get_strategy = BetasGetStrategy()
        single_base = get_strategy.get_single_base(self.config, ['cg00001249', 'cg00001261', 'cg00001269'])

        self.assertEqual((3, 341), single_base.shape)

    def test_betas_get_strategy_check_aux(self):
        load_strategy = BetasLoadStrategy()
        load_strategy.load(self.config, [])

        get_strategy = BetasGetStrategy()
        aux = get_strategy.get_aux(self.config, 'cg00824141')

        self.assertEqual('FHL2', aux)
