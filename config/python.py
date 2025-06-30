""" python deps for this project """

import config.shared

scripts: dict[str,str] = {
    "pycmdtools": "pycmdtools.main:main",
}
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
build_requires: list[str] = config.shared.PBUILD
test_requires: list[str] = config.shared.PTEST
types_requires: list[str] = [
    "types-PyYAML",
    "pandas-stubs",
    "lxml-stubs",
    "types-beautifulsoup4",
    "types-tqdm",
    "types-jsonschema",
]
requires = install_requires + build_requires + test_requires + types_requires
