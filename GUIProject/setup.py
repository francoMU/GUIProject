from pathlib import Path

import versioneer
from setuptools import find_packages, setup

with open(Path(__file__).parent / "requirements.txt", "r") as file:
    requirements = file.readlines()

setup(
    name='GUIProject',
    description="A PyQt5 GUI application",
    author="Franco Peter Moitzi",
    author_email='franco.moitzi@mcl.at',
    url='https://github.com/francoMU/GUIProject',
    packages=find_packages(),
    install_requires=requirements,
    package_data={
        'guiproject.images': ['*.png'],
        'guiproject.data': ['*.txt', '*.gz', '.h5']
    },
    entry_points={
        'console_scripts': ['guiproject=guiproject.application:main']
    },
    zip_safe=False,
    keywords='GUIProject',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
