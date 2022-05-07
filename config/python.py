import config.project

package_name = config.project.project_name

console_scripts = [
    "pycmdtools=pycmdtools.main:main",
]

install_requires = [
    "pylogconf",
    "pytconf",
    "requests",
    "tqdm",
    "numpy",
    "pandas",
    "unidecode",
    "pyyaml",
    "jsonschema",
    "pytidylib",
    "beautifulsoup4",
    "lxml",
]

test_requires = [
    "pylint",
    "pytest",
    "pytest-cov",
    "flake8",
    "pymakehelper",
]

dev_requires = [
    "pyclassifiers",
    "pypitools",
    "pydmt",
    "Sphinx",
]

python_requires = ">=3.9"
test_os = ["ubuntu-20.04"]
test_python = ["3.9"]
