# Installation

Make sure you have the latest version of pip
```
python -m pip install --upgrade pip
```

## From local source
```
python -m pip install --user -e .
```
* -m employ pip module for installation (using the python version with which it was invoked)
* --user locally installs the package hence it is not available on the whole system
* -e activates development mode for the package. All changes to the source code
  are reflected in the package once it is reloaded.
* . references the current working directory which should be the root directory of the tptp package
  
* an executable 'tptp' will be installed in the bin directory of your system or user space.
  On Ubuntu this location is ~/.local/bin if installed with --user.
  The executable is not deleted if the package is uninstalled.

## From PyPi Test Repo
```
python -m pip install --extra-index-url https://test.pypi.org/simple/ tptp==0.0.3.dev1
```

## From PyPi Repo
```
asd
```

# Deinstallation
```
python -m pip uninstall tptp
```
Be aware the python REPL adds the current working directory to the python PATH
making the tptp package available even if it is not installed 
but the current working directory is the tptp package directoy.

# Invocation
* calling the main method of the module with
```
python -m tptp
```
* using the executable 'tptp'

# Packaging
Install twine
```
python -m pip install twine
```
Create a distribution
```
python setup.py sdist bdist_wheel
```
Check distribution
```
twine check dist/*
```
Upload to PyPi Test Repo
```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```
Upload to PyPi Repo
```
twine upload dist/*
```