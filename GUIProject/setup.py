from setuptools import setup

requirements = [
    # TODO: put your package requirements here
]

setup(
    name='GUIProject',
    version='0.0.1',
    description="A PyQt5 GUI application",
    author="Franco",
    author_email='franco.moitzi@mcl.at',
    url='https://github.com/francoMU\/GUIProject',
    packages=['guiproject', 'guiproject.images',
              'guiproject.tests'],
    package_data={'guiproject.images': ['*.png']},
    entry_points={
        'console_scripts': [
            'Template=guiproject.application:main'
        ]
    },
    install_requires=requirements,
    zip_safe=False,
    keywords='GUIProject',
    classifiers=[
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
