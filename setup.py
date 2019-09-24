import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README_CONTENT = (HERE / "README.md").read_text(encoding='utf-8')


setup(name='tptp',
    version='0.0.3-dev2',
    description='A library for handling TPTP related input and systems',
    description_content_type='text/plain',
    long_description=README_CONTENT,
    long_description_content_type='text/markdown',
    author='Tobias Gleißner',
    author_email='tobias.gleissner@fu-berlin.de',
    url='https://github.com/leoprover/tptp',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.5',
    #keywords='TPTP',
    license='BSD3',
    packages=find_packages(),
    #package_data={'': ['*.json','*.tex']},
    install_requires=[
        'pathlib',
        'lxml',
        'requests',
        'colorama',
        #'antlr4-python3-runtime==4.7.1',
    ],
    #include_package_data=True,
    entry_points={
    'console_scripts': [
        'tptp = tptp.frontend.bin.__main__:main'
        ]
    }
)
