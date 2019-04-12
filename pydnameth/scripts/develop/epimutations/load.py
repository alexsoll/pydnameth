import copy
from pydnameth.config.config import Config
from pydnameth.config.experiment.types import DataType
from pydnameth.config.experiment.experiment import Experiment
from pydnameth.config.attributes.attributes import Attributes
from pydnameth.config.annotations.annotations import Annotations
from pydnameth.infrastucture.load.epimutations import load_epimutations


def epimutations_load_dev(data):

    config = Config(
        data=copy.deepcopy(data),
        experiment=Experiment(
            type=DataType.epimutations,
            task=None,
            method=None,
            params=None
        ),
        annotations=Annotations(
            name='annotations',
            exclude='bad_cpgs',
            cross_reactive='any',
            snp='any',
            chr='NS',
            gene_region='any',
            geo='any',
            probe_class='any'
        ),
        attributes=Attributes(
            target=None,
            observables=None,
            cells=None
        ),
        is_run=True,
        is_root=True
    )

    load_epimutations(config)
