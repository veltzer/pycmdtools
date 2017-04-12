import setuptools

import sys
if not sys.version_info[0] == 3:
    sys.exit("Sorry, only python version 3 is supported")

setuptools.setup(
    name='pycmdtools',
    version='0.0.11',
    description='pycmdtools is set of useful command line tools written in python',
    long_description='pycmdtools is set of useful command line tools written in python',
    url='https://veltzer.github.io/pycmdtools',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='python command line shell utilities',
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    install_requires=[
        'click',  # for command line parsing
    ],
    entry_points={
        'console_scripts': [
            'pycmdtools_uniq=pycmdtools.scripts.uniq:main',
            'pycmdtools_mcmp=pycmdtools.scripts.mcmp:main',
        ],
    },
)
