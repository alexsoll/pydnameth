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
from pydnameth.infrastucture.load.residuals import load_residuals
from pydnameth.infrastucture.path import get_data_base_path


class TestLoadResiduals(unittest.TestCase):

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

    def tearDown(self):
        path = get_data_base_path(self.config)
        exts = ('.npz', '.pkl')
        for root, dirs, files in os.walk(path):
            for currentFile in files:
                if currentFile.lower().endswith(exts):
                    os.remove(os.path.join(root, currentFile))

    def test_load_residuals_check_files_creation(self):
        suffix = 'cells(' + str(self.config.attributes.cells) + ')'
        fn_dict = get_data_base_path(self.config) + '/' + 'residuals_dict_' + suffix + '.pkl'
        fn_data = get_data_base_path(self.config) + '/' + 'residuals_' + suffix + '.npz'

        load_residuals(self.config)

        self.assertEqual(True, os.path.isfile(fn_dict) and os.path.isfile(fn_data))

    def test_load_residuals_check_len_cpg_dict(self):
        load_residuals(self.config)
        self.assertEqual(300, len(list(self.config.residuals_dict)))

    def test_load_residuals_check_shape_cpg_data(self):
        load_residuals(self.config)
        self.assertEqual((300, 729), self.config.residuals_data.shape)
