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
from pydnameth.infrastucture.load.residuals_common import load_residuals_common
from tests.tear_down import clear_cache
from pydnameth.infrastucture.path import get_data_base_path


class TestLoadResidualsCommon(unittest.TestCase):

    def setUp(self):

        data = Data(
            name='cpg_beta',
            path=ROOT_DIR,
            base='fixtures'
        )

        experiment = Experiment(
            type=None,
            task=None,
            method=None,
            params=None
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

    def test_load_residuals_check_files_creation(self):
        suffix = 'cells(' + str(self.config.attributes.cells) + ')'
        fn_dict = get_data_base_path(self.config) + '/' + 'residuals_dict_' + suffix + '.pkl'
        fn_data = get_data_base_path(self.config) + '/' + 'residuals_' + suffix + '.npz'

        load_residuals_common(self.config)

        self.assertEqual(True, os.path.isfile(fn_dict) and os.path.isfile(fn_data))

    def tearDown(self):
        clear_cache(self.config)

    def test_load_residuals_check_len_cpg_dict(self):
        load_residuals_common(self.config)
        self.assertEqual(300, len(list(self.config.residuals_dict)))

    def test_load_residuals_check_shape_cpg_data(self):
        load_residuals_common(self.config)
        self.assertEqual((300, 729), self.config.residuals_data.shape)
