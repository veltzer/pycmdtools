import config.project

package_name = config.project.project_name

console_scripts = [
    'pycmdtools_change_first_line=pycmdtools.scripts.change_first_line:main',
    'pycmdtools_count=pycmdtools.scripts.count:main',
    'pycmdtools_find_bad_symlinks=pycmdtools.scripts.find_bad_symlinks:main',
    'pycmdtools_google_drive_download=pycmdtools.scripts.google_drive_download:main',
    'pycmdtools_mcmp=pycmdtools.scripts.mcmp:main',
    'pycmdtools_print_all_args=pycmdtools.scripts.print_all_args:main',
    'pycmdtools_remove_bad_symlinks=pycmdtools.scripts.remove_bad_symlinks:main',
    'pycmdtools_stats=pycmdtools.scripts.stats:main',
    'pycmdtools_uniq=pycmdtools.scripts.uniq:main',
    'pycmdtools_validate_json=pycmdtools.scripts.validate_json:main',
    'pycmdtools_validate_yaml=pycmdtools.scripts.validate_yaml:main',
    'pycmdtools_progress=pycmdtools.scripts.progress:main',
    'pycmdtools_sample_weighted=pycmdtools.scripts.sample_weighted:main',
]

setup_requires = [
]

run_requires = [
    'pylogconf',
    'requests',
    'tqdm',
    'click',
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
