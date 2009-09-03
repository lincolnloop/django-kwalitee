# pulled from django.test.utils in 1.1
# function does not exist in 1.0
def get_runner(settings):
    if isinstance(settings, str):
        test_runner_str = settings
    else:
        test_runner_str = settings.TEST_RUNNER
    test_path = test_runner_str.split('.')
    # Allow for Python 2.5 relative paths
    if len(test_path) > 1:
        test_module_name = '.'.join(test_path[:-1])
    else:
        test_module_name = '.'
    test_module = __import__(test_module_name, {}, {}, test_path[-1])
    test_runner = getattr(test_module, test_path[-1])
    return test_runner