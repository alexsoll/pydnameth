import unittest
from tests.definitions import ROOT_DIR
from pydnameth import Data
from pydnameth import Experiment
from pydnameth import Annotations
from pydnameth import Observables
from pydnameth import Cells
from pydnameth import Attributes
from pydnameth import Config
from pydnameth.infrastucture.load.excluded import load_excluded
from pydnameth.config.annotations.types import AnnotationKey
from pydnameth.config.annotations.conditions import exclude_condition
from pydnameth.config.annotations.conditions import snp_condition
from pydnameth.config.annotations.conditions import gene_region_condition
from pydnameth.config.annotations.conditions import probe_class_condition


class TestAnnotationsConditions(unittest.TestCase):
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
            experiment=experiment,
            annotations=annotations,
            attributes=attributes,
            is_run=True,
            is_root=True
        )

    def test_exclude_condition(self):
        self.config.excluded = load_excluded(self.config)
        ex_cpg = {AnnotationKey.cpg.value: 'cg00000165'}
        is_not_excluded = exclude_condition(self.config, ex_cpg)
        self.assertEqual(False, is_not_excluded)

    def test_snp_condition(self):
        annotations_dict = {AnnotationKey.Probe_SNPs.value: 'rs12616624',
                            AnnotationKey.Probe_SNPs_10.value: 'rs35342923'}
        condition1 = snp_condition(self.config, annotations_dict)

        annotations_dict = {AnnotationKey.Probe_SNPs.value: '',
                            AnnotationKey.Probe_SNPs_10.value: 'rs35342923'}
        condition2 = snp_condition(self.config, annotations_dict)

        annotations_dict = {AnnotationKey.Probe_SNPs.value: 'rs12616624',
                            AnnotationKey.Probe_SNPs_10.value: ''}
        condition3 = snp_condition(self.config, annotations_dict)

        self.assertEqual(False, condition1 or condition2 or condition3)

    def test_gene_region_condition(self):
        annotations_dict = {AnnotationKey.gene.value: ['PRR4', 'TAS2R20']}
        condition1 = gene_region_condition(self.config, annotations_dict)

        annotations_dict = {AnnotationKey.gene.value: []}
        condition2 = gene_region_condition(self.config, annotations_dict)

        self.assertEqual((True, False), (condition1, condition2))

    def test_probe_class_condition(self):
        annotations_dict = {AnnotationKey.probe_class.value: 'A'}
        condition1 = probe_class_condition(self.config, annotations_dict)

        annotations_dict = {AnnotationKey.probe_class.value: 'B'}
        condition2 = probe_class_condition(self.config, annotations_dict)

        annotations_dict = {AnnotationKey.probe_class.value: 'C'}
        condition3 = probe_class_condition(self.config, annotations_dict)

        annotations_dict = {AnnotationKey.probe_class.value: 'D'}
        condition4 = probe_class_condition(self.config, annotations_dict)

        annotations_dict = {AnnotationKey.probe_class.value: ''}
        condition5 = probe_class_condition(self.config, annotations_dict)

        self.assertEqual((True, True, False, False, False),
                         (condition1, condition2, condition3, condition4, condition5))


if __name__ == '__main__':
    unittest.main()
