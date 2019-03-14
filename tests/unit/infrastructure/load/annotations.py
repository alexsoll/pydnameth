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
from pydnameth.infrastucture.load.annotations import load_annotations_dict
from pydnameth.config.annotations.types import AnnotationKey
from pydnameth.infrastucture.path import get_data_base_path


class TestLoadAnnotations(unittest.TestCase):

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

    def compare_cross_r_cpg(self, cpg_list, ann_dict):
        compare = True
        for cpg in cpg_list:
            index = ann_dict[AnnotationKey.cpg.value].index(cpg)
            if not ann_dict[AnnotationKey.cross_reactive.value][index]:
                compare = False
                break
        return compare

    def test_load_annotations_dict_num_elems(self):
        annotations_dict = load_annotations_dict(self.config)
        self.assertEqual(len(annotations_dict['ID_REF']), 300)

    def test_load_annotations_dict_num_keys(self):
        annotations_dict = load_annotations_dict(self.config)
        self.assertEqual(len(list(annotations_dict.keys())), 10)

    def test_load_annotations_dict_num_chrs(self):
        annotations_dict = load_annotations_dict(self.config)
        self.assertEqual(len(set(annotations_dict['CHR'])), 11)

    def test_load_annotations_dict_num_bops(self):
        annotations_dict = load_annotations_dict(self.config)
        self.assertEqual(len(set(annotations_dict['BOP'])), 82)

    def test_load_annotations_check_pkl_file_creation(self):
        load_annotations_dict(self.config)

        create = os.path.isfile(self.config.data.path + '/' + self.config.data.base + '/' +
                                self.config.annotations.name + '.pkl')

        self.assertEqual(True, create)

    def test_load_annotations_num_cross_r_cpgs(self):
        annotations_dict = load_annotations_dict(self.config)

        num_of_cross_r_cpg = sum(list(map(int, annotations_dict[AnnotationKey.cross_reactive.value])))

        self.assertEqual(num_of_cross_r_cpg, 22)

    def test_load_annotations_dict_compare_cross_r_cpg(self):
        cross_r_cpg = ['cg03242964', 'cg06142509', 'cg06352932', 'cg07110474', 'cg07208077', 'cg07818063',
                       'cg08555389', 'cg08683088', 'cg09720033', 'cg11032157', 'cg14502651', 'cg14829303',
                       'cg14894369', 'cg18241189', 'cg20188490', 'cg20418818', 'cg21752292', 'cg22505295',
                       'cg22805813', 'cg23146713', 'cg24653967', 'cg25677688']
        annotations_dict = load_annotations_dict(self.config)

        compare = self.compare_cross_r_cpg(cross_r_cpg, annotations_dict)

        self.assertEqual(True, compare)

    def test_load_annotations_dict_num_geo(self):
        annotations_dict = load_annotations_dict(self.config)
        num_geo = len(set(annotations_dict[AnnotationKey.geo.value]))

        self.assertEqual(6, num_geo)

    def test_load_annotations_dict_num_class(self):
        annotations_dict = load_annotations_dict(self.config)
        self.assertEqual(len(set(annotations_dict[AnnotationKey.probe_class.value])), 4)


if __name__ == '__main__':
    unittest.main()
