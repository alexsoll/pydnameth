.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/AaronBlare/pydnameth/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

pydnameth could always use more documentation, whether as part of the
official pydnameth docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/AaronBlare/pydnameth/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up ``pydnameth`` for local development.


Environment
~~~~~~~~~~~
We use `Anaconda`_ Python distribution and `PyCharm`_ IDE

You can use any other Python distributions and IDEs.

.. _Anaconda: https://www.anaconda.com
.. _PyCharm: https://www.jetbrains.com/pycharm/


GitHub Init
~~~~~~~~~~~

1. Fork the ``pydnameth`` repo on GitHub.

2. `Travis CI`_ and `AppVeyor`_  are continuous integration tools.
   Login using your Github credentials.
   It may take a few minutes for Travis CI and AppVeyor to load up a list of all your GitHub repos.
   Turn on testing your origin repository on Travis CI and AppVeyor.
   To do this, log into your personal account, synchronize the repositories with GitHub
   and add ``pydnameth`` project.

.. _Travis CI: https://travis-ci.org
.. _AppVeyor: https://www.appveyor.com

Local
~~~~~

1. Clone your fork locally::

    $ git clone git@github.com:your_name_here/pydnameth.git

2. Create a virtual environment for your project and activate it::

    $ conda create --name your-env-name python=x.x
    $ activate your-env-name

   where ``your-env-name`` is the name you want to call your environment,
   and replace ``x.x`` with the Python version you wish to use (for example 3.7)

3. Go to the root of ``pydnameth`` project and install project in 'editable'
   or 'develop' mode while you’re working on it and install all libs ``requirements_dev.txt``::

    $ pip install --editable .
    $ pip install -r requirements_dev.txt

   ``.`` refers to the current working directory.
   This allows the project to be both installed and editable in project form.

3. If with some package ``err-pkg`` error occurs, try::

    $ conda install err-pkg --channel=conda-forge

   And repeat command::

    $ pip install -r requirements_dev.txt

4. If ``requirements_dev.txt`` file was updated, you should repeat the command::

    $ pip install -r requirements_dev.txt

Git Pipeline
~~~~~~~~~~~~


1. ``master`` branch is always in production, tested and complete.
2. ``development`` is the branch closest to ``master`` but has changes that should be merged to ``master``.
   Anyone who starts working on a new feature should or bug fixing always branch out from ``development``.
3. Branch out from ``development`` with new branch for bug or feature::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

4. When you're done making changes, check that your changes pass flake8 and the
   tests::

    $ tox

5. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the GitHub website.

Pull Request Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.7, 3.6 and 3.5. Check
   https://travis-ci.org/AaronBlare/pydnameth/pull_requests
   and make sure that the tests pass for all supported Python versions.

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in ``HISTORY.rst``).
Then run::

    $ git add HISTORY.rst
    $ git commit -m "Changelog for upcoming release x.x.x."
    $ bumpversion patch # possible: major / minor / patch
    $ git push
    $ git push --tags

Travis will then deploy to PyPI if tests pass.
