from pydnameth.infrastucture.load.annotations import load_annotations_dict
from pydnameth.infrastucture.load.excluded import load_excluded
from pydnameth.infrastucture.load.attributes import load_attributes_dict
from pydnameth.infrastucture.load.attributes import load_cells_dict
from pydnameth.config.annotations.subset import subset_annotations
from pydnameth.config.attributes.subset import subset_attributes
from pydnameth.config.attributes.subset import subset_cells, get_indexes


class Config:

    def __init__(self,
                 data,
                 experiment,
                 annotations,
                 attributes,
                 is_run=True
                 ):

        self.data = data
        self.experiment = experiment
        self.annotations = annotations
        self.attributes = attributes
        self.is_run = is_run

        self.cpg_gene_dict = {}
        self.cpg_bop_dict = {}
        self.gene_cpg_dict = {}
        self.gene_bop_dict = {}
        self.bop_cpg_dict = {}
        self.bop_gene_dict = {}

        self.cpg_list = []
        self.cpg_dict = {}
        self.cpg_data = []

        self.gene_list = []
        self.gene_dict = {}
        self.gene_data = []

        self.bop_list = []
        self.bop_dict = {}
        self.bop_data = []

        self.attributes_indexes = []

        self.excluded = None

        self.annotations_dict = None
        self.attributes_dict = None
        self.attributes_indexes = None
        self.cells_dict = None

    def __str__(self):
        name = f'data({str(self.data)})_' \
               + f'experiment({str(self.experiment)})_' \
               + f'annotations({str(self.annotations)})_' \
               + f'attributes({str(self.attributes)})'
        return name

    def set_hash(self, hash):
        self.hash = hash

    def initialize(self):

        self.excluded = load_excluded(self)

        self.annotations_dict = load_annotations_dict(self)
        subset_annotations(self)

        self.attributes_dict = load_attributes_dict(self)
        self.attributes_indexes = get_indexes(self)
        subset_attributes(self)
        self.cells_dict = load_cells_dict(self)
        subset_cells(self)
