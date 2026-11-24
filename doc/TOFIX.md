# TOFIX

Findings from a code scan on 2026-10-04.

## Medium

- `src/pycmdtools/utils.py:107` - `gdrive_download_link` (behind the `google_drive_download_by_url` command) never downloads anything: it fetches the share page, `print`s it through BeautifulSoup and returns, although its docstring promises to extract the file id/name and download it; finish it (parse the id and call `download_file_from_google_drive`) or remove the command.
- `pyproject.toml:41` - `numpy`, `pandas`, `unidecode` (line 43) and `pytidylib` (line 48) are runtime dependencies of the published package but nothing under `src/` imports them (pandas/numpy/unidecode appear only in `doc/sample_weighted.py.doc`, tidylib only in commented-out code at `src/pycmdtools/utils.py:124`); drop them so installing the CLI does not pull in pandas/numpy.
- `src/pycmdtools/main.py:489` - `parser.errors = error_handler` has no effect: html5lib's `HTMLParser._parse()` calls `reset()`, which sets `self.errors = []`, so the handler is overwritten before parsing starts and never called; remove it (strict mode already raises `ParseError`) or read `parser.errors` after a non-strict parse to report all errors.

## Low

- `src/pycmdtools/main.py:160` - the `progress` command is registered but its body is only a docstring, so it silently does nothing (likewise `xprofile_select` at line 369 just prints "TBD"); unregister unfinished commands until they are implemented (the idea is already in `doc/TODO.txt`).
- `src/pycmdtools/main.py:187` - `stats` accumulates `total_sum2` but never uses it and prints only the mean, though the command is described as "Print statistics"; print count/mean/stddev or drop the dead accumulator.
- `src/pycmdtools/python.py:181` - the `if check_with is None` error branch is unreachable (line 179 has just set it to `"python3"`); and a syntax error makes `subprocess.check_output` (line 189) raise `CalledProcessError` with a traceback, so the "no output" check at line 196 never reports anything; catch the error and report it cleanly.
- `src/pycmdtools/utils.py:97` - HTTP status checks use `assert` (also line 122), which vanish under `python -O`; use `response.raise_for_status()`.
- `src/pycmdtools/main.py:345` - command description typo "jsonschame".
- `pyproject.toml:93` - `mypy_path = "src:python:scripts"` names `python` and `scripts` directories that do not exist; reduce to `src`.
- `doc/TODO.txt:8` - "make setup.py be made out of a template" is obsolete (the project builds with hatchling from `pyproject.toml`; there is no setup.py); remove the item.
