=====
Usage
=====

Import
------

To use pydnameth in a project:

.. code-block:: python

    import pydnameth as pdm

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


Experiments
-----------

All experiments provided py ``pydnameth`` are divided into 3 types:

* ``pdm.base`` - use only methylation data
* ``pdm.advanced`` - use methylation data and results of any other experiments
* ``pdm.plot`` - use methylation data and results of any other experiments

For each experiment, it is necessary to create one main instance of the ``pdm.Config`` class.
For ``pdm.advanced`` and ``pdm.plot`` experiments it is necessary to create additional instances of the ``pdm.Config`` class for primary experiments,
which results uses it target experiment.

Config
------

For creating instance of the ``pdm.Config`` you need to create additional instances:

* ``pdm.Data``
* ``pdm.Setup``
* ``pdm.Annotations``
* ``pdm.Attributes``

Data
~~~~

``pdm.Data`` contains information about dataset and the type of data that will be used in the experiments.
For creating instance of ``pdm.Data`` you need to specify next fields:

* ``name`` - name of the file without extension (currently supported only ``.txt`` extension),
  which contains methylation data. Example: ``name='cpg_beta'``
* ``type`` - instance of ``enum`` ``pdm.DataType``.
  Indicates type of data that will be used in the experiments.
  Currently supported only ``pdm.DataType.cpg`` and ``pdm.DataType.attributes``.
  In next releases ``pdm.DataType.gene`` and ``pdm.DataType.bop`` will be added. Example: ``type=pdm.DataType.cpg``
* ``path`` - path to directory, which contains ``base`` directory.
  Example: ``path=C:/Data``
* ``base`` - name of the directory in which the necessary files are located and in which the files with the results will be saved.
  Example: ``base=GSE40279``

Example of creating ``pdm.Data`` instance:

.. code-block:: python

     data = pdm.Data(
        name='cpg_beta',
        type=pdm.DataType.cpg,
        path='C:/Data',
        base='GSE40279'
    )

Setup
~~~~~

``pdm.Setup`` describes the run experiment.
For creating instance of ``pdm.Data`` you need to specify next fields:

* ``name`` - name of the file without extension (currently supported only ``.txt`` extension),
  which contains methylation data. Example: ``name='cpg_beta'``
* ``type`` - instance of ``enum`` ``pdm.DataType``.
  Indicates type of data that will be used in the experiments.
  Currently supported only ``pdm.DataType.cpg`` and ``pdm.DataType.attributes``.
  In next releases ``pdm.DataType.gene`` and ``pdm.DataType.bop`` will be added. Example: ``type=pdm.DataType.cpg``
* ``path`` - path to directory, which contains ``base`` directory.
  Example: ``path=C:/Data``
* ``base`` - name of the directory in which the necessary files are located and in which the files with the results will be saved.
  Example: ``base=GSE40279``

Example of creating ``pdm.Data`` instance:

.. code-block:: python

     data = pdm.Data(
        name='cpg_beta',
        type=pdm.DataType.cpg,
        path='C:/Data',
        base='GSE40279'
    )

