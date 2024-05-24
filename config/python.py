from typing import List


console_scripts: List[str] = [
    "pycmdtools=pycmdtools.main:main",
]
dev_requires: List[str] = [
    "pypitools",
    "black",
]
config_requires: List[str] = [
    "pyclassifiers",
]
install_requires: List[str] = [
    "pylogconf",
    "pytconf",
    "requests",
    "types-requests",
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
build_requires: List[str] = [
    "pymakehelper",
    "pydmt",
    "pandas-stubs",
    "lxml-stubs",
    "types-beautifulsoup4",
    "types-tqdm",
    "types-jsonschema",
]
test_requires: List[str] = [
    "pylint",
    "pytest",
    "pytest-cov",
    "flake8",
    "mypy",
    "types-PyYAML",
]
requires = config_requires + install_requires + build_requires + test_requires
