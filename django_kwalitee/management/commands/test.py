import sys
from optparse import make_option

from django.core import management
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import get_apps

from django_kwalitee.testrunners import get_runner

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--noinput', action='store_false', dest='interactive', 
            default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'),
        make_option('--coverage', action='store_true', dest='coverage', 
            default=False,
            help='Show coverage details'),
        make_option('--local', action='store_true', dest='local',
            default=False,
            help='Only test "local" apps (submodules of the project).')
    )
    help = """Custom test command which allows for 
        specifying different test runners."""
    args = '[appname ...]'

    requires_model_validation = False

    def handle(self, *test_labels, **options):

        verbosity = int(options.get('verbosity', 1))
        interactive = options.get('interactive', True)
        
        # it's quite possible someone, lets say South, might have stolen
        # the syncdb command from django. For testing purposes we should
        # probably put it back. Migrations don't really make sense
        # for tests. Actually the South test runner does this too.
        management.get_commands()
        management._commands['syncdb'] = 'django.core'

        if options.get('coverage'):
            test_runner_name = 'django_kwalitee.testrunners.codecoverage.run_tests'
        else:
            test_runner_name = settings.TEST_RUNNER
        
        # hack to run subset of full test suite
        # just use test_labels to load up non-excluded apps
        if options.get('local') and not test_labels:
            local_apps = []
            for app in get_apps():
                app_label = app.__name__.split('.')[-2]
                if not app_label in settings.KWALITEE_LOCAL_EXCLUDES:
                    local_apps.append(app_label)
            test_labels = tuple(local_apps)
        
        test_runner = get_runner(test_runner_name)

        failures = test_runner(test_labels, verbosity=verbosity, 
            interactive=interactive)
        if failures:
            sys.exit(failures)