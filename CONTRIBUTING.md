# Contributing to MSS Packages

## Introduction
Adding your algorithm to _msspackages_ is easy with the following steps.  

## Adding Your Algorithm to _msspackages_
It is assumed that you have already cloned the _msspackages_ __main__ branch to your local machine for your use.  If you have not done this already, this is covered in the [_README_](README.md) file.  As standard with _git_, you need to have the main branch cloned inorder to create a branch.

### Creating a Branch
Perform the following commands within your _msspackages_ repository:

1. Get a fresh pull on the the _msspackages_ repository:
```console
$ git pull
```

2. Next, create a branch from _main_ on your local machine by executing following command; you will need to replace the fields with your first name and the name of your algorithm:
```console
$ git branch firstname/name_of_algo
```
__For Example__: If Vinny put together a brand new algorithm for creating buckets with EKS data, his branch and command would look as follows:
```console
$ git branch vinny/bucketization
```
3. Now, you are still working in the _main_ branch on your local machine.  This can be confirmed by issuing the _branch_ command which will show the current branch as highlighted:
```console
$ git branch
```
4. You will now need to switch your branch to the new branch you created.  To do this, execute the following command, replacing _firstname/name_of_algo_ with your previously defined branch name:
```console
$ git switch firstname/name_of_algo
```
5. Confirm you are now working in your branch by issuing the branch command:
```console
$ git branch
```
6. Now, you will need to push your current branch and set it as the upstream equivalent.  This will add your branch held on your local machine to the repository online:
```console
$ git push --set-upstream origin firstname/name_of_algo
```

### Adding Your Algorithm to The Directory Hierarchy
Adding your algorithm to the _msspackages_ library is a relatively easy process; however, it is important that the steps below are followed closely to ensure the new algorithm builds in correctly to the existing framework.  To make things easy to follow, an example algorithm ___circles___ has been included as an example to follow.

#### 1. Create a New Directory Under the [_msspackages_](/msspackages/) Sub-Directory
Navigate to the _msspackages_ sub-directory within the _msspackages_ repository:
```console
> msspackages
    > msspackages
        __init__.py
        > [OtherPackages]
```
Here, create a new directory.  The directory should be named with your algorithm name, the same name you included in the branch you checked out above.  For the _circles_ sub-package, the new directory would be titled as follows:
```console
> msspackages
    > msspackages
        __init__.py
        > circles
        > [OtherPackages]
```
This new folder is the sub-package folder for your algorithm.

#### 2. Add Your Algorithm and __init__ File to the Sub-Package
This directory is where your algorithm will be stored.  You will also need an _init_ file in this directory - this _init_file allows access to your Python file when building the package. So, following the _circles_ sub-package, the directory structure would look as follows:

```console
> msspackages
    > msspackages
        __init__.py
        > circles
            __init__.py
            CirclesClass.py
        > [OtherPackages]
```
#### 3. Add Needed Information to __init__ Files
This step is very important for ensuring your sub-package is able to interact correctly with the rest of the _msspackages_ structure and be available for use when the package is installed.  For this step, work from the sub-package level (in the example, the __init__ file __within__ the _circles_ directory) up to the root of the _msspackages_ repository.

This example is following a simple class that is being added to the package.  You as the developer make the decision on what functions and classes of your code should be available for use with the package and what should not be.  You will also need to make the decision on what level of dot notation will be needed in order to access specific aspects of your code.  This is covered in detail below. 

**Sub-Package __init__ File**:

The __init__ file is used in Python to give access to aspects of your code from a higher level.  The general process is to explicitly elevate functions and classes that should be accessible at the level of the directory in-which the __init__ file resides.  Here is an example to illustrate this point:

Following the _circles_ example from earlier, I have written a useful class called _Circle_ located in _CirclesClass.py_.  In the Python file, there are several class methods as well as a function outside of the class for describing circles:
```python
import math

class Circle:
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color

    def get_radius(self):
        return self.radius

    def get_color(self):
        return self.color
     
    def area(self):
        return math.pi*(self.radius*self.radius)

    def perimeter(self):
        return 2*math.pi*self.radius

def describe(circle):
    print(f"This is a {circle.color} circle with a radius of {circle.radius}.")
``` 
When I contribute this code to _msspackages_, my hope is to have both the class _Circle_ and the function _describe_ available for use at a minimum level of the _circles_ sub-package directory.  This means that if I am to import the _msspackages_ library as follows, I should be able to access both the class and function with the following syntax:

**Desired Syntax**
```python
import msspackages as mss
# this is how I want to be able to use Circle and describe
ci = mss.circles.Circle(radius, color)

mss.circles.describe(ci)
```
But since there is currently nothing in the __init__ file, in order to access the _describe_ function and _Circle_ class, the following notation would be needed to access the class and function:

**Current Syntax**
```python
import msspackages as mss
# this is how you currently access Circle and describe
ci = mss.circles.CirclesClass.Circle(radius, color)

mss.circles.CirclesClass.Circle(ci)
```
As you can see, as the syntax currently sits, using the class and function require quite verbose calls.  However, the following use of the __init__ files eliminates the need to call the ___CirclesClass___ in the dot notation.  That's because the _describe_ function and _Circles_ class reside in _CirclesClass.py_ and are not directly present in the _circles_ directory, but including them in the __init__ file as follows effectively adds them there:

As a reminder, we are adding these to the inner __init__ file within the _circles_ directory:
```console
> msspackages
    > msspackages
        __init__.py
        > circles
            __init__.py
            CirclesClass.py
        > [OtherPackages]
```
To elevate _Circles_ and _describe_ to the _circles_ directory, add the following to the the __init__ file:

```python
# msspackages/msspackages/circles/__init__.py
from .CirclesClass import Circle
from .CirclesClass import describe
```
Next, we need to add some information to the outer __init__ file:

**Package Level __init__ file**:

To complete the initial __init__ file process, the following must be added to the __init__ file within /msspackages/msspackages:

```python
# msspackages/msspackages/__init__.py
from .circles import CirclesClass
```
With the above imports included in the respective __init__ files, the **Desired Syntax** from above can now be used: 

```python
import msspackages as mss
# this syntax will work now
ci = mss.circles.Circle(radius, color)

mss.circles.describe(ci)
```
Now, looking at the existing syntax, I may feel that the syntax is still too verbose in order to make a call to the class _Circle_; however, looking at the _describe_ function, I feel like this syntax is appropriate (I want people to know that _describe_ is only to be used on instances of _Circle_, so leaving the _circles_ dot notation is appropriate).  With this line of thinking, I would like to change the syntax to the following:

**New Desired Syntax**:
```python
import msspackages as mss
# I want to shorten the syntax for creating an instance of Circle
ci = mss.Circle(radius, color)

# and keep the syntax the same for calling describe
mss.circles.describe(ci)
```
To do this, I simply add the following to the **Package Level __init__ file**:
```python
# msspackages/msspackages/__init__.py

# existing imports:
from .circles import CirclesClass

# add this line to shorten the sytax to mss.Circles(radius, color):
from .circles import Circle
```
This effectively pulls only the class _Circle_ up to the level of _msspackages_ while leaving the _describe_ function at the level of the _circles_ directory.  So once these imports in the __init__ files are completed, the following syntax will be valid:

```python
import msspackages as mss

ci = mss.Circle(radius, color)

mss.circles.describe(ci)
```
Here are the example __init__ files for completeness and clarity:

**__init__ file in _msspackages_ directory**:
```python
# msspackages/msspackages/__init__.py
from .circles import CirclesClass
from .circles import Circle
```
**__init__ file in _circles_ directory**:
```python
# msspackages/msspackages/circles/__init__.py
from .CirclesClass import Circle
from .CirclesClass import describe
```

#### 2. Add Dependencies to [_requirements.txt_](requirements.txt)

Add all dependencies included in your algorithm / sub-package in the [_requirements.txt_](requirements.txt) file.  You must also include the package version number for your dependency.  This locks down the version you are using and prevents version conflicts if present.

Add your dependencies with the following format, this is taken directly from the existing [_requirements.txt_](requirements.txt) file:

```python
pandas==1.4.3
numpy==1.23.1
tqdm==4.64.0
```
If your version specific dependencies are already included in the list, do not duplicate them.

#### 3. Modify the [_setup.py_](setup.py) File
There are two points in the [_setup.py_](setup.py) that will need to be edited to incorporate your sub-package into _msspackages_.

First, you will add your package directory to the _find_packages_ field.  To do this, add your package name with the format of ___msspackages.PackageDirectoryName___ to the _include_ list.  Simply add a comma after the last item and include the formatted package name as a string as specified above.

__For example__ if the _packages=find_packages_ field is currently set with the following list:
```python
packages=find_packages(include=['msspackages', 'msspackages.extras']),
```
and I want to add the ___circles___ sub-package, I would make the following addition to the list:
```python
packages=find_packages(include=['msspackages', 'msspackages.extras', 'msspackages.circles'])
```
Second, you will need to add any dependencies included in the [_requirements.txt_](requirements.txt) to the _install_requires_ list.  The version number is required to be included just like with the _requirements.txt_ file:

```python
install_requires=['pandas==1.4.3',
                      'numpy==1.23.1',
                      'tqdm==4.64.0'
                      ]
```

### Adding Your Test Cases


#### Test File Setup
In order to maintain the integrity of the _msspackages_ library, grow the set of algorithms sustainably, and future proof the code with increased maintainability, all new algorithms are required to include unit tests.  This is the process of testing each aspect/function of the code individually to gain insight to how each aspect of the code in performing and make the process of debugging much easier.

In _msspackages_ the [_pytest_](https://docs.pytest.org/en/7.1.x/) framework is used to create a simple and scalable testing environment. Below are examples of how to implement unit tests for your algorithm based on the _circles_ example above.

All unit tests must be stored in the [_tests_](/tests/) directory at the root of the _msspackages_ structure. In this directory, create a Python file with the naming format as follows:
```console
> msspackages
    > msspackages
    > tests
        test_<AlgoName>.py
```
Replace _AlgoName_ with the name of your algorithm, this should match the algorithm name you included on your branch.

For the _circles_ example, the test file looks as follows:
```console
>msspackages
    > msspackages
    >tests
        test_circles.py
```
__Note__: The **test_** prefix to the Python test file is crucial to ensure successful testing with Pytest. 

Next, you will need to write the unit tests in the _test_circles.py_ file:

#### Writing Unit Tests
The idea of unit tests is to test each aspect of your code.  With this in mind, the unit tests for the [_circles_](msspackages/circles/CirclesClass.py) sub-package of _msspackages_ are written as follows:

```python
from msspackages import circles

ci = circles.Circle(5, 'red')

def test_describe():
    assert circles.describe(ci) == print('this is a red circle.')
def test_getters():
    assert ci.get_radius() == 5
    assert ci.get_color() == 'red'
def test_area():
    assert ci.area() == 78.53981633974483
def test_perimeter():
    assert ci.perimeter() == 31.41592653589793
```
The general process is as follows:  

1. Pull in the sub-package you are testing (i.e. your sub-package included in _msspackages_)
2. For each class and function in your sub-package, create a test function
3. The test function should contain the same *test_* prefix 
4. Within the test function, an **assertion** must be made to test against

The test function format can be generalized as follows:

```python
def test_FunctionInPackage():
    assert FunctionInPackage(input) == ExpectedOutPut
```
#### Run the Unit Tests
When your test functions are complete, you can run the test cases by navigating to the _msspackages_ root and executing the following command:
```console
~/msspackages$ pytest
```
the _pytest_ command must be within the same directory that the ___tests___ directory is located.  Once run, _pytest_ will generate output on the test.
## Test Building _msspacakges_ With your Sub-Pacakge
It is time for a test build!  If you've followed the steps above, and your unit tests are all passing, then it's time to test-build _msspackages_ with your sub-package on your local machine.  This involves the following steps:

1. [Uninstall _msspackages_ from your pip package manager](#uninstall-msspacages-from-local-host)
2. [Compile a new .whl file including your sub-package](#build-whl-file)
3. [Install the new wheel file using pip](#install-new-whl-file)
4. [Test the features of your sub-package](#test-the-sub-package)

### Uninstall _msspacages_ from Local Host
Issue the following command in your terminal to remove the existing install of _msspackages_:
```console
$ pip uninstall msspackages
```
### Build _.whl_ File
Navigate to the root of the _msspacakges_ directory you have been working in on your local host.  Then issue the following command:
```console
~/msspackages$ python setup.py bdist_wheel
```
This will generate the .whl file in the _dist_ directory at the root of the _msspackages_ file structure.
### Install New _.whl_ File
Next, from the same directory, execute the following command:
```console
~/msspackages$ pip install /dist/*.whl
```
**Note:** in Windows, you will need to hit ___tab___ prior to executing the above command, this will autocomplete the name of the _.whl_ file. 

### Test the Sub-Package
Now navigate to your home directory to get out of the _msspackages_ folder, this will ensure that you are testing _msspackages_ off of the pip installed version, not the _msspackages_ directory:
```console
$ cd ~
```
Now, enter a Python Environment and test your sub-package.  Try various levels of imports, test all the features, and ensure everything is behaving as it should.  For example, the _cricles_ sub-packge would be tested as follows
```console
>>> from msspackages import circles as ci
>>> mycircle = ci.Circle(2, "red")
>>> mycircle.radius
2
>>> mycircle.color
'red'
>>> ci.describe(mycircle)
This is a red circle with a radius of 2.
```
If everything in your algorithm is functioning as expected, then it's time time to submit a merge request to have your code included in the next release of _msspacakges_!

## Submitting a Pull Request