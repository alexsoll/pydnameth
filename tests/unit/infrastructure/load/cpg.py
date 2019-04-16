import unittest
import os
from tests.definitions import ROOT_DIR
from pydnameth.config.data.data import Data
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.config.annotations.annotations import Annotations
from pydnameth.config.attributes.attributes import Observables
from pydnameth.config.attributes.attributes import Cells
from pydnameth.config.attributes.attributes import Attributes
from pydnameth.config.config import Config
from pydnameth.infrastucture.load.betas import load_betas
from pydnameth.infrastucture.path import get_data_base_path
from tests.tear_down import clear_cache


class TestLoadCpG(unittest.TestCase):

    def setUp(self):

        data = Data(
            path=ROOT_DIR,
            base='fixtures'
        )

        experiment = Experiment(
            data=None,
            task=None,
            method=None,
        )

        annotations = Annotations(
            name='annotations',
            exclude='none',
            cross_reactive='ex',
            snp='ex',
            chr='NS',
            gene_region='yes',
            geo='any',
            probe_class='any'
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
            experiment=experiment,
            annotations=annotations,
            attributes=attributes,
            is_run=True,
            is_root=True
        )
        self.config.initialize()

    def tearDown(self):
        clear_cache(self.config)

    def test_load_cpg_check_files_creation(self):
        fn_dict = get_data_base_path(self.config) + '/' + 'betas_dict.pkl'
        fn_data = get_data_base_path(self.config) + '/' + 'betas'
        fn_npz = fn_data + '.npz'

        load_betas(self.config)

        self.assertEqual(True, os.path.isfile(fn_dict) and os.path.isfile(fn_npz))

    def test_load_cpg_check_len_cpg_dict(self):
        load_betas(self.config)
        self.assertEqual(300, len(list(self.config.betas_dict)))

    def test_load_cpg_check_shape_cpg_data(self):
        load_betas(self.config)
        self.assertEqual((300, 729), self.config.betas_data.shape)
