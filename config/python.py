""" python deps for this project """

scripts: dict[str,str] = {
    "pycmdtools": "pycmdtools.main:main",
}
config_requires: list[str] = [
    "pyclassifiers",
]
install_requires: list[str] = [
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
    "html5lib",
]
build_requires: list[str] = [
    "hatch",
    "pydmt",
    "pymakehelper",
    "pycmdtools",
]
test_requires: list[str] = [
    "pylint",
    "pytest",
    "mypy",
    "ruff",
    # types
    "types-PyYAML",
    "pandas-stubs",
    "lxml-stubs",
    "types-beautifulsoup4",
    "types-tqdm",
    "types-jsonschema",
]
requires = config_requires + install_requires + build_requires + test_requires
