import config.project
import pydmt.helpers.python

from pycmdtools.endpoints.main import main

package_name = config.project.project_name

console_scripts = [
    pydmt.helpers.python.make_console_script(package_name, main),
]

setup_requires = [
]

run_requires = [
    'pylogconf',
    'pytconf',
    'requests',
    'tqdm',
    'numpy',
    'pandas',
    'unidecode',
    'pyyaml',
]

test_requires = [
    'pylint',  # to check for lint errors
    'pytest',  # for testing
    'pyflakes',  # for testing
]

dev_requires = [
    'pyclassifiers',  # for programmatic classifiers
    'pypitools',  # for upload etc
    'pydmt',  # for building
    'Sphinx',  # for the sphinx builder
]

install_requires = list(setup_requires)
install_requires.extend(run_requires)

python_requires = ">=3.5"

extras_require={
#    ':python_version == "2.7"': ['futures'],  # for python2.7 backport of concurrent.futures
}
