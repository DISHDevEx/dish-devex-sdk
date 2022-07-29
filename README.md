# MSS Packages

## __Features__


### __Deployment features__




## __How to Use__

### __Installation__
1. Navigate to your ***git*** directory on your local machine
2. Clone the repo
```console
$ git clone https://gitlab.global.dish.com/MSS/msspackages.git
```
3. Navigate into the root _msspackages_ directory.
```console
$ cd msspackages
```
4. Run the following command to create the wheel file
 
```console
$ python setup.py bdist_wheel
```
5. Next, pip install the wheel file by running the following command, note that the _version_ will change depending upon the release:
```console
$ pip install /dist/msspackages-(version)-py3-non-any.whl
```
### __Usage__

Once complete, _msspackages_ will be available in your Python evironment for use.  Enter your Python environment and import _msspackages_ as you would with any other library or package.
```console
>>> import msspackages as mss
```
All functions contained in _msspackages_ available for use can be listed by listing the package directory structure, using the alias of _mss_ specified on import:
```console
>>> dir(mss)
```
The package and included functions can then be used like any other Python library.  Functions can be used via dot notation with the specified packages:
```conscole
>>> mss.multiply(2,3)
6
```
Alternatively, you can import all algorithms from the _msspackages_ library and use each without the use of dot notation:
```console
>>> from msspackages import *
>>> multiply(2,3)
6
```

## __History__
View verion history and release notes in [HISTORY](HISTORY.md). 

## __Contributing__
Learn how about [CONTRIBUTING](CONTRIBUTING.md) to MSS Packages.


