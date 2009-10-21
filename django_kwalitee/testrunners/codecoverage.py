import coverage
import os
import re
from inspect import getmembers, ismodule

from django.conf import settings
from django.db.models import get_app, get_apps

from django_kwalitee.testrunners import get_runner

def get_all_coverage_modules(app_module):
    """
    Returns all possible modules to report coverage on, even if they
    aren't loaded.
    """
    # We start off with the imported models.py, so we need to import
    # the parent app package to find the path.
    app_path = app_module.__name__.split('.')[:-1]
    app_package = __import__('.'.join(app_path), {}, {}, app_path[-1])
    app_dirpath = app_package.__path__[-1]

    mod_list = []
    for root, dirs, files in os.walk(app_dirpath):
        root_path = app_path + root[len(app_dirpath):].split(os.path.sep)[1:]
        for fyle in files:
            if fyle.lower().endswith('.py'):
                mod_name = fyle[:-3].lower()
                mod_str = '.'.join(root_path + [mod_name])

                matches = True
                for regex in getattr(settings, 'KWALITEE_COVERAGE_EXCLUDES', []):
                    if re.search(regex, mod_str):
                        matches = False
                        break

                if matches:
                    try:
                        mod = __import__(mod_str, {}, {}, mod_name)
                        mod_list.append(mod)
                    except ImportError:
                        pass

    return mod_list

def run_tests(test_labels, verbosity=1, interactive=True,
        extra_tests=[]):
    """
    Test runner which displays a code coverage report at the end of the
    run.
    """
    django_test_runner = get_runner(settings)
    coverage.use_cache(0)
    coverage.start()
    
    results = django_test_runner(test_labels, verbosity, interactive, 
        extra_tests)
    coverage.stop()

    coverage_modules = []
    if test_labels:
        for label in test_labels:
            # Don't report coverage if you're only running a single
            # test case.
            if '.' not in label:
                app = get_app(label)
                coverage_modules.extend(get_all_coverage_modules(app))
    else:
        for app in get_apps():
            coverage_modules.extend(get_all_coverage_modules(app))

    if coverage_modules:
        coverage.report(coverage_modules, show_missing=1)

    return results
    
