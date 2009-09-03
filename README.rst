A growing suite of scripts to measure the "kwalitee [1]_" of a Django project. These are designed to be used in an automated `continuous integration <http://en.wikipedia.org/wiki/Continuous_integration>`_ environment.

lint.py
=======

A wrapper around `pylint <http://pypi.python.org/pypi/pylint>`_ that analyzes a Django project file by file and calculates a weighted average based on lines of code for the whole project. It tweaks the pylint runs on the fly to accommodate for expected Django usage that doesn't necessarily follow pylint's guidelines.

In early usage, we find that an average rating of 7/10 or higher can be considered "good."

Usage::

    lint.py [path/to/my_project]
    
**To Do**:

* More tweaking of pylint flags
* set ``MINIMUM_SCORE`` & ``EXCLUDE_DIRS`` via flags at runtime


Custom Test Runner
==================

The custom test runner was largely "borrowed" from Gareth Rushgrove's `django-test-extensions <http://github.com/garethr/django-test-extensions>`_. It utilizes `coverage.py <http://pypi.python.org/pypi/coverage/>`_ to provide coverage reports on your test suite.

An additional option (``--local``) has been added to allow you to limit the tests and coverage reports. We frequently want to know what the coverage is on code *we* wrote and not include Django itself or 3rd-party applications. ``--local`` expects a setting ``EXCLUDE_FROM_LOCAL_TESTS`` that is a list of application labels to skip when running the test suite. If you store your local applications within your project module, a line like this will suffice::

    KWALITEE_LOCAL_EXCLUDES = [app.split('.')[-1] for app in INSTALLED_APPS \
                                          if not app.startswith('[my_project]')]
                                          
.. note:: Replace ``[my_project]`` with the name of your project.

Some common modules really shouldn't be reported via ``coverage`` as they skew the results. These can be excluded via regular expressions on the module name. We typically use the following::

    KWALITEE_COVERAGE_EXCLUDES = (r'\.tests(\.|$)', 
                                  r'\.migrations\.',
                                  r'\.evolutions\.')
                                  
**Usage:**

#. Add ``django_kwalitee`` to your ``INSTALLED_APPS``.
#. ``./manage.py test --help``
    
**To do:**

* Pass minimum coverage requirement in via the options and exit with a failure if they are not met.


Similar Projects
----------------

This project was inspired by the following projects. There is overlap, but for one reason or another, they didn't quite fit our needs.

* `cheesecake <http://pycheesecake.org>`_
* `django-lint <http://chris-lamb.co.uk/projects/django-lint/>`_
* `django-test-extensions <http://github.com/garethr/django-test-extensions>`_


.. [1] http://cpants.perl.org/kwalitee.html