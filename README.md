# DevEx SDK

### __Installing devex_sdk__ from PyPi (Latest Release):
```console
pip install devex-sdk
```
or
```console
pip install git+https://github.com/DISHDevEx/dish-devex-sdk.git
```

### __Installing devex_sdk__ from local build (beta testing):
1. Navigate into the root _devex_sdk_ directory.
```console
cd dish-devex-sdk
```
2. Run the following command to create the wheel file
 
```console
python setup.py bdist_wheel --version <VERSION_NUMBER>
```
**NOTE**: the ***<VERSION_NUMBER>*** only effects your local build.  You can use any version number you like.  This can be helpful in testing prior to submitting a pull request.  Alternatively, you can exclude the ***--version <VERSION_NUMBER>*** flag and the .whl file name will output as ***devex_sdk-_VERSION_PLACEHOLDER_-py3-none-any.whl***

3. Next, pip install the wheel file by running the following command, note that the _version_ will change depending upon the release:
```console
pip install /dist/devex_sdk-<VERSION_NUMBER>-py3-none-any.whl
```
### __Usage__

Once complete, _devex_sdk_ will be available in your Python evironment for use.  Enter your Python environment and import _devex_sdk_ as you would with any other library or package.
```console
>>> import devex_sdk
```
All functions contained in _devex_sdk_ available for use can be listed by listing the package directory structure:
```console
>>> dir(devex_sdk)
```
The package and included functions can then be used like any other Python library.  Functions can be used via dot notation with the specified packages:
```conscole
>>> devex_sdk.multiply(2,3)
6
```
Alternatively, you can import all algorithms from the _devex_sdk_ library and use each without the use of dot notation:
```console
>>> from devex_sdk import *
>>> multiply(2,3)
6
```

## __History__
View version history and release notes in [HISTORY](https://github.com/DISHDevEx/dish-devex-sdk/blob/main/HISTORY.md). 

## __Contributing__
Learn how about [CONTRIBUTING](https://github.com/DISHDevEx/dish-devex-sdk/blob/main/CONTRIBUTING.md) to devex_sdk.

## __Releases on GitHub__
View all [DevEx SDK releases](https://github.com/DISHDevEx/dish-devex-sdk/releases) on GitHub.

## __Releases on PyPi__
View all [DevEx SDK release](https://pypi.org/project/devex-sdk/#history) history on PyPi.


## Python Packages in DevEx SDK
- [Data Ingestion](https://github.com/DISHDevEx/dish-devex-sdk/tree/main/devex_sdk/data_ingestion)
- [Feature Engine](https://github.com/DISHDevEx/dish-devex-sdk/tree/main/devex_sdk/feature_engine)
- [Bucketization](https://github.com/DISHDevEx/dish-devex-sdk/tree/main/devex_sdk/bucketization)
