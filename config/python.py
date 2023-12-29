console_scripts = [
    "pycmdtools=pycmdtools.main:main",
]
dev_requires = [
    "pypitools",
]
config_requires = [
    "pyclassifiers",
]
install_requires = [
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
make_requires = [
    "pymakehelper",
    "pydmt",
    "pyclassifiers",
    "pandas-stubs",
    "lxml-stubs",
    "types-beautifulsoup4",
    "types-tqdm",
    "types-jsonschema",
]
test_requires = [
    "pylint",
    "pytest",
    "pytest-cov",
    "flake8",
    "mypy",
    "types-PyYAML",
]
requires = config_requires + install_requires + make_requires + test_requires
