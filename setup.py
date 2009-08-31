from setuptools import setup, find_packages

setup(
    name = "django-kwalitee",
    version = "0.1",
    packages = find_packages('src'),
    scripts = ['src/lint.py'],
)