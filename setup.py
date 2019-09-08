import pathlib
from setuptools import setup
from setuptools import find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(name='tptp',
    version='0.0.0',
    description='A library for handling TPTP related input and systems',
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ],
    #keywords='asd',
    license='BSD3',
    packages=find_packages(),
    #package_data={'': ['*.json','*.tex']},
    install_requires=[
        'pathlib',
        'lxml',
        'requests',
        #'antlr4-python3-runtime==4.7.1',
    ],
    #include_package_data=True,
    #entry_points={
    #'console_scripts': [
    #    'foo = system_on_tptp.main'
    #    ]
    #}
)