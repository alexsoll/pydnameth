
.. image:: https://img.shields.io/pypi/v/pydnameth.svg
    :target: https://pypi.python.org/pypi/pydnameth
    :alt: PyPi page

.. image:: https://travis-ci.org/AaronBlare/pydnameth.svg?branch=master
    :target: https://travis-ci.org/AaronBlare/pydnameth
    :alt: Travis build status

.. image:: https://ci.appveyor.com/api/projects/status/22k49b00nql1gi5j/branch/master?svg=true
    :target: https://ci.appveyor.com/project/AaronBlare/pydnameth
    :alt: Appveyor build status

.. image:: https://codecov.io/gh/AaronBlare/pydnameth/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/AaronBlare/pydnameth
    :alt: Coverage status

.. image:: https://img.shields.io/lgtm/grade/python/g/AaronBlare/pydnameth.svg?logo=lgtm&logoWidth=18
    :target: https://lgtm.com/projects/g/AaronBlare/pydnameth/context:python
    :alt: LGTM code quality

.. image:: https://pyup.io/repos/github/AaronBlare/pydnameth/shield.svg
    :target: https://pyup.io/repos/github/AaronBlare/pydnameth/
    :alt: Updates

.. image:: https://readthedocs.org/projects/pydnameth/badge/?version=latest
    :target: https://pydnameth.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://badges.gitter.im/AaronBlare/pydnameth.png
    :target: https://gitter.im/pydnameth/community
    :alt: Project Chat


=========
pydnameth
=========

DNA Methylation Analysis Package

This package provides some pipelines for analysis mythylation data.
The main goal is to find correlations between methylation on the one hand,
and age, sex, disease, and other characteristics of subjects on the other.

Examples of free-access methylation datasets:

* `GSE40279`_
* `GSE87571`_

.. _GSE40279: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE40279
.. _GSE87571: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE87571


Documentation
-------------
Available at https://pydnameth.readthedocs.io.

Features
--------

* Defining best age-predictors CpGs for different subjects subsets.
* Defining best observable-specic CpGs (sex-specific, disease-specific) which are differently methylated with age.
* Building Epigenetic Clock.
* Plotting subjects distribution depending on the observable (sex, disease).
* Plotting methylation profiles for CpGs.

Copyrights
----------
Free software: MIT license
