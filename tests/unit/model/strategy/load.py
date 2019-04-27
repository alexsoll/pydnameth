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
from pydnameth.config.experiment.types import Task
from pydnameth.config.experiment.types import DataType
from pydnameth.config.experiment.types import Method
from tests.tear_down import clear_cache


class TestLoadStrategy(unittest.TestCase):
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
            probe_class='A_B'
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

    def tearDown(self):
        clear_cache(self.config)

    def test_betas_load_strategy_base_dict_len(self):
        strategy = BetasLoadStrategy()

        strategy.load(self.config, [])

        self.assertEqual(300, len(self.config.base_dict))

    def test_betas_load_strategy_base_data_len(self):
        strategy = BetasLoadStrategy()

        strategy.load(self.config, [])

        self.assertEqual(300, len(self.config.base_data))
