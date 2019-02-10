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

These files must be located in the same directory. After running experiments, new directories with results
and cached data files with ``.pkl`` and ``.npz`` extensions will appear in this directory.

For all experiments provided by ``pydnameth`` you need to specify config information.

------
Config
------
For each experiment you need to create instances:

* ``pdm.Data``
* ``pdm.Annotations``
* ``pdm.Attributes``

~~~~
Data
~~~~
``pdm.Data`` contains information about dataset.
For creating instance of ``pdm.Data`` you need to specify next fields:

++++++++
``name``
++++++++
Name of the file without extension (currently supported only ``.txt`` extension),
which contains methylation data.

Example::

    name = 'cpg_beta'

++++++++
``path``
++++++++
Path to directory, which contains ``base`` directory.

Example::

    path = 'C:/Data'

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
        path='C:/Data',
        base='GSE40279'
    )

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

``pdm.Attributes`` describes information about subjects.
For creating instance of ``pdm.Attributes`` you need to specify next fields:

++++++++++
``target``
++++++++++
Name of target observable column (``string``)

Example::

    target = 'age'

+++++++++++++++
``observables``
+++++++++++++++
Specifies observables of subjects under consideration. Should be ``pdm.Observables`` instance.
For creating ``pdm.Observables`` instance you need to specify:

* ``name`` - name of the file without extension (currently supported only ``.txt`` extension),
  which contains information about subjects.

Example::

    name = 'observables'

* ``types`` - python ``dict`` with ``key`` - header of target observable and ``value`` - value of target observable.
  Also values can be ``'any'`` if you want to consider all existing values.

Example::

    {'gender': 'F'}

+++++++++
``cells``
+++++++++
Specifies cell types population. Should be ``pdm.Cells`` instance.
For creating ``pdm.Cells`` instance you need to specify:

* ``name`` - name of the file without extension (currently supported only ``.txt`` extension),
  contains information about cell types population.

Example::

    name = 'cells'

* ``types`` - python ``list`` of cell types which should be considered in the experiment (``string`` headers in ``file_name``)
  or string ``'any'`` if you want to consider all cells types.

Example::

    types = ['Monocytes', 'B', 'CD4T', 'NK', 'CD8T', 'Gran']

+++++++
Example
+++++++

Example of creating ``pdm.Attributes`` instance:

.. code-block:: python

    observables = pdm.Observables(
        name='observables',
        types={'gender': 'F'}
    )

    cells = pdm.Cells(
        name='cells',
        types='any'
    )

    attributes = pdm.Attributes(
        target='age',
        observables=observables,
        cells=cells
    )

--------------------
Released Experiments
--------------------
The name of the functions provided by the ``pydnameth`` package are follow the next logic:

* First part is data type for the experiment. For example ``cpg`` or ``attributes``.
* Second part answers the question ``WHAT WE WANT TO DO?``.
  For example ``proc_table`` - table with data and characteristics processing,
  ``plot_methylation`` - methylation data plotting.
* Third part answers the question ``HOW WE WANT TO DO?``. Specifies the method for the experiment.
  For example ``linreg`` - linear regression method.

Currently released functions:

.. automodule:: pydnameth.scripts.release
    :members:




--------------
Usage Examples
--------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
attributes_plot_observables_histogram
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import pydnameth as pdm

    data = pdm.Data(
        name='cpg_beta',
        path='C:/Data',
        base='GSE87571'
    )

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

    observables = pdm.Observables(
        name='observables',
        types={}
    )

    cells = pdm.Cells(
        name='cells',
        types='any'
    )

    attributes = pdm.Attributes(
        target='age',
        observables=observables,
        cells=cells
    )

    observables_list = [
        {'gender': 'F'},
        {'gender': 'M'}
    ]

    pdm.attributes_plot_observables_histogram(
        data=data,
        annotations=annotations,
        attributes=attributes,
        observables_list=observables_list,
        params={
            'bin_size': 1.0,
            'opacity': 0.75,
            'barmode': 'overlay'
        }
    )

~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cpg_plot_methylation_scatter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import pydnameth as pdm

    cpg_list = [
        'cg13982318',
        'cg11868595',
        'cg08900404'
    ]

    data = pdm.Data(
        name='cpg_beta',
        path='C:/Data',
        base='GSE87571'
    )

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

    observables = pdm.Observables(
        name='observables',
        types={}
    )

    cells = pdm.Cells(
        name='cells',
        types='any'
    )

    attributes = pdm.Attributes(
        target='age',
        observables=observables,
        cells=cells
    )

    observables_list = [
        {'gender': 'F'},
        {'gender': 'M'}
    ]

    pdm.cpg_plot_methylation_scatter(
        data=data,
        annotations=annotations,
        attributes=attributes,
        observables_list=observables_list,
        cpg_list=cpg_list,
        params={
            'x_range': [10, 110]
        }
    )

~~~~~~~~~~~~~~~~~~~~~
cpg_proc_clock_linreg
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import pydnameth as pdm

    data = pdm.Data(
        name='cpg_beta',
        path='C:/Data',
        base='GSE87571'
    )

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

    cells = pdm.Cells(
        name='cells',
        types='any'
    )

    obs_list = [
        {'gender': 'F'},
        {'gender': 'M'},
        {'gender': 'any'}
    ]

    for obs in obs_list:

        observables = pdm.Observables(
            name='observables',
            types=obs
        )

        attributes = pdm.Attributes(
            target='age',
            observables=observables,
            cells=cells
        )

        pdm.cpg_proc_clock_linreg(
            data=data,
            annotations=annotations,
            attributes=attributes,
            params={
                'type': 'all',
                'part': 0.25,
                'size': 100,
                'runs': 100,
            }
        )

~~~~~~~~~~~~~~~~~~~~~
cpg_proc_table_linreg
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import pydnameth as pdm

    data = pdm.Data(
        name='cpg_beta',
        path='C:/Data',
        base='GSE87571'
    )

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

    cells = pdm.Cells(
        name='cells',
        types='any'
    )

    obs_list = [
        {'gender': 'F'},
        {'gender': 'M'},
        {'gender': 'any'}
    ]

    for obs in obs_list:

        observables = pdm.Observables(
            name='observables',
            types=obs
        )

        attributes = pdm.Attributes(
            target='age',
            observables=observables,
            cells=cells
        )

        pdm.cpg_proc_table_linreg(
            data=data,
            annotations=annotations,
            attributes=attributes
        )


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cpg_proc_table_variance_linreg
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import pydnameth as pdm

    data = pdm.Data(
        name='cpg_beta',
        path='C:/Data',
        base='GSE87571'
    )

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

    cells = pdm.Cells(
        name='cells',
        types='any'
    )

    obs_list = [
        {'gender': 'F'},
        {'gender': 'M'},
        {'gender': 'any'}
    ]

    for obs in obs_list:

        observables = pdm.Observables(
            name='observables',
            types=obs
        )

        attributes = pdm.Attributes(
            target='age',
            observables=observables,
            cells=cells
        )

        pdm.cpg_proc_table_variance_linreg(
            data=data,
            annotations=annotations,
            attributes=attributes
        )


~~~~~~~~~~~~~~~~~~~~~~
cpg_proc_table_polygon
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import pydnameth as pdm

    data = pdm.Data(
        name='cpg_beta',
        path='C:/Data',
        base='GSE87571'
    )

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

    observables = pdm.Observables(
        name='observables',
        types={}
    )

    cells = pdm.Cells(
        name='cells',
        types='any'
    )

    attributes = pdm.Attributes(
        target='age',
        observables=observables,
        cells=cells
    )

    observables_list = [
        {'gender': 'F'},
        {'gender': 'M'}
    ]

    pdm.cpg_proc_table_polygon(
        data=data,
        annotations=annotations,
        attributes=attributes,
        observables_list=observables_list
    )

~~~~~~~~~~~~~~~~~~~~~~~~~~~~
cpg_proc_table_z_test_linreg
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import pydnameth as pdm

    data = pdm.Data(
        name='cpg_beta',
        path='C:/Data',
        base='EPIC'
    )

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

    observables = pdm.Observables(
        name='observables',
        types={}
    )

    cells = pdm.Cells(
        name='cells',
        types='any'
    )

    attributes = pdm.Attributes(
        target='age',
        observables=observables,
        cells=cells
    )

    observables_list = [
        {'gender': 'F'},
        {'gender': 'M'}
    ]

    pdm.cpg_proc_table_z_test_linreg(
        data=data,
        annotations=annotations,
        attributes=attributes,
        observables_list=observables_list
    )
