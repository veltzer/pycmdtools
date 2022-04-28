#import pydmt.helpers.python

import config.project
from pycmdtools.main import main

package_name = config.project.project_name

console_scripts = [
    'pycmdtools=pycmdtools.main:main',
#    pydmt.helpers.python.make_console_script(package_name, main),
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
    'jsonschema',
    'pytidylib',
    'beautifulsoup4',
    'lxml',
]

test_requires = [
    'pylint',
    'pytest',
    'pytest-cov',
    'flake8',
    'pymakehelper',
]

dev_requires = [
    'pyclassifiers',
    'pypitools',
    'pydmt',
    'Sphinx',
]

install_requires = list(setup_requires)
install_requires.extend(run_requires)

python_requires = ">=3.7"

extras_require = {
}
test_os = "[ubuntu-18.04, ubuntu-20.04]"
test_python = "[3.7, 3.8, 3.9]"
test_container = "[ 'ubuntu:18.04', 'ubuntu:20.04' ]"
