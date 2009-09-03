from setuptools import setup, find_packages

setup(
    name = "django-kwalitee",
    version = "0.1",
    packages = find_packages(),
    package_data = {'django_kwalitee':['bin/*.*']},
    exclude_package_data = {'django_kwalitee':['bin/*.pyc']},
    scripts = ['django_kwalitee/bin/lint.py'],
    install_requires=[
        'pylint',
        'coverage',
    ]
)
