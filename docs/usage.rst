=====
Usage
=====

------
Import
------
To use pydnameth in a project:

.. code-block:: python

    import pydnameth as pdm

----
Info
----
As a rule, 4 files are provided in each methylation dataset:

* ``cpg_beta.txt`` - contains methylation data itself.
  Rows correspond to individual CpGs, and columns correspond to subjects.
* ``annotations.txt`` - contains information about CpGs.
  Rows correspond to individual CpGs, and columns correspond to CpG's characteristics (gene, bop, coordinate, etc.).
* ``observables.txt`` - contains information about subjects.
  Rows correspond to subjects, and columns correspond to subject's observables (age, gender, disease, etc.).
* ``cells.txt`` - contains information about cell types population.
  For example, if DNA methylation profiles taken from human whole blood,
  then for each patient a different proportion of blood cells types is possible.
  Rows in file correspond to subjects, and columns correspond different cell types proportions.

The first line in each file is usually a header. File names and file extensions may differ, but content is the same.
Currently supported only ``.txt`` extension.

All experiments provided py ``pydnameth`` running by single function ``pdm.run(config, configs_primary)``.
For each experiment, it is necessary to create one main instance of the pdm.Config class (described below).
For some experiments it is necessary to create additional instances of the pdm.Config class for primary experiments, which results uses it main experiment.

------
Config
------
For creating instance of the ``pdm.Config`` you need to create additional instances:

* ``pdm.Data``
* ``pdm.Setup``
* ``pdm.Annotations``
* ``pdm.Attributes``

~~~~
Data
~~~~
``pdm.Data`` contains information about dataset and the type of data that will be used in the experiments.
For creating instance of ``pdm.Data`` you need to specify next fields:

++++++++
``name``
++++++++
Name of the file without extension (currently supported only ``.txt`` extension),
which contains methylation data.

Example::

    name = 'cpg_beta'

++++++++
``type``
++++++++
Indicates type of data that will be used in the experiments. Instance of ``enum`` ``pdm.DataType``
Currently supported only ``pdm.DataType.cpg`` and ``pdm.DataType.attributes``.
In next releases ``pdm.DataType.gene`` and ``pdm.DataType.bop`` will be added.

Example::

    type = pdm.DataType.cpg

++++++++
``path``
++++++++
Path to directory, which contains ``base`` directory.

Example::

    path = C:/Data

++++++++
``base``
++++++++
Name of the directory in which the necessary files are located and in which the files with the results will be saved.

Example::

    base = 'GSE40279'

+++++++
Example
+++++++
Example of creating ``pdm.Data`` instance:

.. code-block:: python

     data = pdm.Data(
        name='cpg_beta',
        type=pdm.DataType.cpg,
        path='C:/Data',
        base='GSE40279'
    )

~~~~~
Setup
~~~~~

``pdm.Setup`` describes the run experiment using the following hierarchy.
For creating instance of ``pdm.Setup`` you need to specify each level of hierarchy:

++++++++++++++
``experiment``
++++++++++++++

Type of the experiment, specifies ``TYPE OF RESEARCH`` (top-level of hierarchy). It should be instance of ``enum`` ``pdm.Experiment``.
Currently supported 3 main types of experiment:

* ``pdm.Experiment.base`` - use only methylation data.
* ``pdm.Experiment.advanced`` - use methylation data and results of any other experiments.
* ``pdm.Experiment.plot`` - use methylation data and results of any other experiments.

Example::

    experiment = pdm.Experiment.base

++++++++
``task``
++++++++
Specifies ``WHAT WE WANT TO DO`` (mid-level of hierarchy). It should be instance of ``enum`` ``pdm.Task``. Currently supported tasks:

* ``pdm.Experiment.table`` - creating table with different measurables.
  Can be used for ``pdm.Experiment.base`` and ``pdm.Experiment.advanced``.
* ``pdm.Experiment.clock`` - building epigenetic clock.
  Can be used only for ``pdm.Experiment.advanced``.
* ``pdm.Experiment.observables`` - perform analysis with subject's observables.
  Can be used only for ``pdm.Experiment.plot``.
* ``pdm.Experiment.methylation`` - perform analysis with raw methylation data.
  Can be used only for ``pdm.Experiment.plot``.

Example::

    task = pdm.Experiment.table

++++++++++
``method``
++++++++++
Specifies ``HOW WE WANT TO DO`` (bottom-level hierarchy).
It should be instance of ``enum`` ``pdm.Method``. Currently supported tasks:

* ``pdm.Method.linreg`` - perform linear regression between target observable and choosen ``pdm.DataType``.
  Can be used for ``pdm.Experiment.table`` and  ``pdm.Experiment.clock``.
* ``pdm.Method.variance_linreg`` - perform linear regression for variance
  from linear regression line between target observable and chosen ``pdm.DataType``.
  Can be used for ``pdm.Experiment.table``
* ``pdm.Method.cluster`` - clustering on plane of target observable and chosen ``pdm.DataType``.
  Can be used for ``pdm.Experiment.table``
* ``pdm.Method.histogram`` - creating figures with histograms.
  Can be used for ``pdm.Experiment.observables``
* ``pdm.Method.scatter`` - creating figures with scatters.
  Can be used for ``pdm.Experiment.methylation``
* ``pdm.Method.polygon`` - allows to define observable-specific markers.
  Can be used for ``pdm.Experiment.table``

Example::

    method = pdm.Method.linreg

++++++++++
``params``
++++++++++
Specifies params for chosen combination of  ``task`` and ``method``.
It should be ``dict`` where ``key`` is the name of param and ``value`` is the value of param.
You can leave it empty - in this case, the params settings are used.

Example::

    params = {}

+++++++
Example
+++++++

Example of creating ``pdm.Setup`` instance:

.. code-block:: python

     setup = pdm.Setup(
        experiment=pdm.Experiment.base,
        task=pdm.Task.table,
        method=pdm.Method.linreg,
        params={}
    )

More information in `More Details About Methods`_ and `Released`_ sections

~~~~~~~~~~~
Annotations
~~~~~~~~~~~

``pdm.Annotations`` allows you to define a subset of CpGs that will be considered in the experiment.
For creating instance of ``pdm.Annotations`` you need to specify next fields:

++++++++
``name``
++++++++
Name of the file without extension (currently supported only ``.txt`` extension),
which contains information about CpGs.

Example::

    name = 'annotations'

+++++++
exclude
+++++++

Name of the file without extension (currently supported only ``.txt`` extension),
which contains CpGs to exclude.
If equals to ``'none'``, then no excluded CpGs.

Example::

    exclude = 'none'

++++++++++++++
cross_reactive
++++++++++++++

Should cross-reactive CpGs be considered in the experiment?
Currently supported options (``string``):

* ``'ex'`` - excluded all cross-reactive CpGs.
* ``'any'`` - all CpGs are considered.


Example::

    cross_reactive = 'ex'

+++
snp
+++

Should SNP CpGs be considered in the experiment?
Currently supported options (``string``):

* ``'ex'`` - excluded all SNP CpGs.
* ``'any'`` - all CpGs are considered.


Example::

    snp = 'ex'

+++
chr
+++

What chromosomes are considered in the experiment?
Currently supported options (``string``):

* ``'NS'`` - CpGs only on non-sex chromosomes are considered.
* ``'X'`` - CpGs only on X chromosome are considered.
* ``'Y'`` - CpGs only on Y chromosome are considered.
* ``'any'`` - all CpGs are considered.

Example::

    chr = 'NS'

+++++++++++
gene_region
+++++++++++

Should we consider CpGs which are mapped on genes?
Currently supported options (``string``):

* ``'yes'`` - only CpGs which are mapped on genes are considered.
* ``'no'`` - only CpGs which are not mapped on genes are considered.
* ``'any'`` - all CpGs are considered.

Example::

    gene_region = 'yes'

+++
geo
+++

CpGs on what geo-types should be considered?
Currently supported options (``string``):

* ``'shores'`` - only CpGs on shores are considered.
* ``'shores_s'`` - only CpGs on southern shores are considered.
* ``'shores_n'`` - only CpGs on northern shores are considered.
* ``'islands'`` - only CpGs on islands are considered.
* ``'islands_shores'`` - only CpGs on islands or shores are considered.
* ``'any'`` - all CpGs are considered.

Example::

    gene_region = 'any'


+++++++++++
probe_class
+++++++++++

What CpGs probe class should be considered?
Currently supported options (``string``):

* ``'A'`` - class A CpGs are considered.
* ``'B'`` - class B CpGs are considered.
* ``'C'`` - class C CpGs are considered.
* ``'D'`` - class D CpGs are considered.
* ``'A_B'`` - class A or B CpGs are considered.
* ``'any'`` - all CpGs are considered.

Example::

    probe_class = 'any'

+++++++
Example
+++++++

Example of creating ``pdm.Annotations`` instance:

.. code-block:: python

    annotations = pdm.Annotations(
        name='annotations',
        exclude='none',
        cross_reactive='ex',
        snp='ex',
        chr='NS',
        gene_region='yes',
        geo='any',
        probe_class='any'
    )

~~~~~~~~~~
Attributes
~~~~~~~~~~

--------------------------
More Details About Methods
--------------------------

--------
Released
--------
