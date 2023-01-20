# DevEx SDK
### __Installing devex_sdk__
1. Navigate into the root _devex_sdk_ directory.
```console
$ cd devex_sdk
```
2. Run the following command to create the wheel file
 
```console
$ python setup.py bdist_wheel
```
3. Next, pip install the wheel file by running the following command, note that the _version_ will change depending upon the release:
```console
$ pip install /dist/devex_sdk-(version)-py3-non-any.whl
```
### __Usage__

Once complete, _devex_sdk_ will be available in your Python evironment for use.  Enter your Python environment and import _devex_sdk_ as you would with any other library or package.
```console
>>> import devex_sdk as mss
```
All functions contained in _devex_sdk_ available for use can be listed by listing the package directory structure, using the alias of _mss_ specified on import:
```console
>>> dir(mss)
```
The package and included functions can then be used like any other Python library.  Functions can be used via dot notation with the specified packages:
```conscole
>>> mss.multiply(2,3)
6
```
Alternatively, you can import all algorithms from the _devex_sdk_ library and use each without the use of dot notation:
```console
>>> from devex_sdk import *
>>> multiply(2,3)
6
```

## __History__
View verion history and release notes in [HISTORY](HISTORY.md). 

## __Contributing__
Learn how about [CONTRIBUTING](CONTRIBUTING.md) to MSS Packages.


