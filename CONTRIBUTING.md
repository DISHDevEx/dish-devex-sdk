# Contributing to DevEx SDK

## Introduction
Adding your algorithm to _devex_sdk_ is easy with the following steps.  

## Adding Your Algorithm to _devex_sdk_
It is assumed that you have already cloned the _devex_sdk_ __main__ branch to your local machine for your use.  If you have not done this already, this is covered in the [_README_](README.md) file.  As standard with _git_, you need to have the main branch cloned inorder to create a branch.

### Creating a Branch
Perform the following commands within your _devex_sdk_ repository:

1. Get a fresh pull on the the _devex_sdk_ repository:
```console
git pull
```

2. Next, create a branch from _main_ on your local machine by executing following command; you will need to replace the fields with your first name and the name of your algorithm:
```console
  git branch firstname/name_of_algo
```
__For Example__: If Vinny put together a brand-new algorithm for creating buckets with EKS data, his branch and command would look as follows:
```console
 git branch vinny/bucketization
```
3. Now, you are still working in the _main_ branch on your local machine.  This can be confirmed by issuing the _branch_ command which will show the current branch as highlighted:
```console
 git branch
```
4. You will now need to switch your branch to the new branch you created.  To do this, execute the following command, replacing _firstname/name_of_algo_ with your previously defined branch name:
```console
 git switch firstname/name_of_algo
```
5. Confirm you are now working in your branch by issuing the branch command:
```console
 git branch
```
6. Now, you will need to push your current branch and set it as the upstream equivalent.  This will add your branch held on your local machine to the repository online:
```console
 git push --set-upstream origin firstname/name_of_algo
```

### Adding Your Algorithm to The Directory Hierarchy
Adding your algorithm to the _devex_sdk_ library is a relatively easy process; however, it is important that the steps below are followed closely to ensure the new algorithm builds in correctly to the existing framework.  To make things easy to follow, an example algorithm ___circles___ has been included as an example to follow.

#### 1. Create a New Directory Under the [_devex_sdk_](/devex_sdk/) Sub-Directory
Navigate to the _devex_sdk_ subdirectory within the _devex_sdk_ repository:
```console
> devex_sdk
    > devex_sdk
        __init__.py
        > [OtherPackages]
```
Here, create a new directory.  The directory should be named with your algorithm name, the same name you included in the branch you checked out above.  For the _circles_ sub-package, the new directory would be titled as follows:
```console
> devex_sdk
    > devex_sdk
        __init__.py
        > circles
        > [OtherPackages]
```
This new folder is the sub-package folder for your algorithm.

#### 2. Add Your Algorithm and __init__ File to the Sub-Package
This directory is where your algorithm will be stored.  You will also need an _init_ file in this directory - this _init_file allows access to your Python file when building the package. So, following the _circles_ sub-package, the directory structure would look as follows:

```console
> devex_sdk
    > devex_sdk
        __init__.py
        > circles
            __init__.py
            CirclesClass.py
        > [OtherPackages]
```
#### 3. Add Needed Information to __init__ Files
This step is very important for ensuring your sub-package is able to interact correctly with the rest of the _devex_sdk_ structure and be available for use when the package is installed.  For this step, work from the sub-package level (in the example, the __init__ file __within__ the _circles_ directory) up to the root of the _devex_sdk_ repository.

This example is following a simple class that is being added to the package.  You as the developer make the decision on what functions and classes of your code should be available for use with the package and what should not be.  You will also need to make the decision on what level of dot notation will be needed in order to access specific aspects of your code.  This is covered in detail below. 

**Sub-Package __init__ File**:

The __init__ file is used in Python to give access to aspects of your code from a higher level.  The general process is to explicitly elevate functions and classes that should be accessible at the level of the directory in-which the __init__ file resides.  Here is an example to illustrate this point:

Following the _circles_ example from earlier, I have written a useful class called _Circle_ located in _CirclesClass.py_.  In the Python file, there are several class methods as well as a function outside the class for describing circles:
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
When I contribute this code to _devex_sdk_, my hope is to have both the class _Circle_ and the function _describe_ available for use at a minimum level of the _circles_ sub-package directory.  This means that if I am to import the _devex_sdk_ library as follows, I should be able to access both the class and function with the following syntax:

**Desired Syntax**
```python
import devex_sdk
# this is how I want to be able to use Circle and describe
ci = devex_sdk.circles.Circle(radius, color)

devex_sdk.circles.describe(ci)
```
But since there is currently nothing in the __init__ file, in order to access the _describe_ function and _Circle_ class, the following notation would be needed to access the class and function:

**Current Syntax**
```python
import devex_sdk
# this is how you currently access Circle and describe
ci = devex_sdk.circles.CirclesClass.Circle(radius, color)

devex_sdk.circles.CirclesClass.Circle(ci)
```
As you can see, as the syntax currently sits, using the class and function require quite verbose calls.  However, the following use of the __init__ files eliminates the need to call the ___CirclesClass___ in the dot notation.  That's because the _describe_ function and _Circles_ class reside in _CirclesClass.py_ and are not directly present in the _circles_ directory, but including them in the __init__ file as follows effectively adds them there:

As a reminder, we are adding these to the inner __init__ file within the _circles_ directory:
```console
> devex_sdk
    > devex_sdk
        __init__.py
        > circles
            __init__.py
            CirclesClass.py
        > [OtherPackages]
```
To elevate _Circles_ and _describe_ to the _circles_ directory, add the following to the __init__ file:

```python
# devex_sdk/devex_sdk/circles/__init__.py
from .CirclesClass import Circle
from .CirclesClass import describe
```
Next, we need to add some information to the outer __init__ file:

**Package Level __init__ file**:

To complete the initial __init__ file process, the following must be added to the __init__ file within /devex_sdk/devex_sdk:

```python
# devex_sdk/devex_sdk/__init__.py
from .circles import CirclesClass
```
With the above imports included in the respective __init__ files, the **Desired Syntax** from above can now be used: 

```python
import devex_sdk
# this syntax will work now
ci = devex_sdk.circles.Circle(radius, color)

devex_sdk.circles.describe(ci)
```
Now, looking at the existing syntax, I may feel that the syntax is still too verbose in order to make a call to the class _Circle_; however, looking at the _describe_ function, I feel like this syntax is appropriate (I want people to know that _describe_ is only to be used on instances of _Circle_, so leaving the _circles_ dot notation is appropriate).  With this line of thinking, I would like to change the syntax to the following:

**New Desired Syntax**:
```python
import devex_sdk
# I want to shorten the syntax for creating an instance of Circle
ci = devex_sdk.Circle(radius, color)

# and keep the syntax the same for calling describe
devex_sdk.circles.describe(ci)
```
To do this, I simply add the following to the **Package Level __init__ file**:
```python
# devex_sdk/devex_sdk/__init__.py

# existing imports:
from .circles import CirclesClass

# add this line to shorten the sytax to devex_sdk.Circles(radius, color):
from .circles import Circle
```
This effectively pulls only the class _Circle_ up to the level of _devex_sdk_ while leaving the _describe_ function at the level of the _circles_ directory.  So once these imports in the __init__ files are completed, the following syntax will be valid:

```python
import devex_sdk

ci = devex_sdk.Circle(radius, color)

devex_sdk.circles.describe(ci)
```
Here are the example __init__ files for completeness and clarity:

**__init__ file in _devex_sdk_ directory**:
```python
# devex_sdk/devex_sdk/__init__.py
from .circles import CirclesClass
from .circles import Circle
```
**__init__ file in _circles_ directory**:
```python
# devex_sdk/devex_sdk/circles/__init__.py
from .CirclesClass import Circle
from .CirclesClass import describe
```

#### 2. Add Dependencies to [_requirements.txt_](requirements.txt)

Add all dependencies included in your algorithm / sub-package in the [_requirements.txt_](requirements.txt) file.  You must also include the package version number for your dependency.  This locks down the version you are using and prevents version conflicts if present.

Add your dependencies with the following format, this is taken directly from the existing [_requirements.txt_](requirements.txt) file:

**Note**: make sure to remember what dependencies you added to the [_requirements.txt_](requirements.txt) file as you will need to add these same dependencies to the [_setup.py_](setup.py) file under *install_requires* in the next step.

```python
pandas==1.4.3
numpy==1.23.1
tqdm==4.64.0
```
If your version specific dependencies are already included in the list, do not duplicate them.

#### 3. Modify the [_setup.py_](setup.py) File
There are two points in the [_setup.py_](setup.py) that will need to be edited to incorporate your sub-package into _devex_sdk_.

***First***, you will add your package directory to the _find_packages_ field.  To do this, add your package name with the format of ___devex_sdk.PackageDirectoryName___ to the _include_ list.  Simply add a comma after the last item and include the formatted package name as a string as specified above.

__For example__ if the _packages=find_packages_ field is currently set with the following list:
```python
packages=find_packages(include=['devex_sdk', 'devex_sdk.extras']),
```
and I want to add the ___circles___ sub-package, I would make the following addition to the list:
```python
packages=find_packages(include=['devex_sdk', 'devex_sdk.extras', 'devex_sdk.circles'])
```
***Second***, you must add any dependencies you added in the [_requirements.txt_](requirements.txt) to the _install_requires_ list.  Only the package name is required to be added here, the version number is not required in this section:

```python
install_requires=['pandas',
                  'numpy',
                  'tqdm',
                      ]
```

### Adding Your Test Cases

#### Test File Setup
In order to maintain the integrity of the _devex_sdk_ library, grow the set of algorithms sustainably, and future proof the code with increased maintainability, all new algorithms are required to include unit tests.  This is the process of testing each aspect/function of the code individually to gain insight to how each aspect of the code in performing and make the process of debugging much easier.

In _devex_sdk_ the [_pytest_](https://docs.pytest.org/en/7.1.x/) framework is used to create a simple and scalable testing environment. Below are examples of how to implement unit tests for your algorithm based on the _circles_ example above.

All unit tests must be stored in the [_tests_](/tests/) directory at the root of the _devex_sdk_ structure. In this directory, create a Python file with the naming format as follows:
```console
> devex_sdk
    > devex_sdk
    > tests
        test_<AlgoName>.py
```
Replace _AlgoName_ with the name of your algorithm, this should match the algorithm name you included on your branch.

For the _circles_ example, the test file looks as follows:
```console
>devex_sdk
    > devex_sdk
    >tests
        test_circles.py
```
__Note__: The **test_** prefix to the Python test file is crucial to ensure successful testing with Pytest. 

Next, you will need to write the unit tests in the _test_circles.py_ file:

#### Writing Unit Tests
The idea of unit tests is to test each aspect of your code.  With this in mind, the unit tests for the [_circles_](devex_sdk/circles/CirclesClass.py) sub-package of _devex_sdk_ are written as follows:

```python
from devex_sdk import circles

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

1. Pull in the sub-package you are testing (i.e. your sub-package included in _devex_sdk_)
2. For each class and function in your sub-package, create a test function
3. The test function should contain the same *test_* prefix 
4. Within the test function, an **assertion** must be made to test against

The test function format can be generalized as follows:

```python
def test_FunctionInPackage():
    assert FunctionInPackage(input) == ExpectedOutPut
```
#### Run the Unit Tests
When your test functions are complete, you can run the test cases by navigating to the _devex_sdk_ root and executing the following command:
RUN: pytest from root dir.
RUN pytest --slow from root dir to run slow tests.
```console
pytest
pytest --slow
```
```
In order to run tests locally please change the bucket_name and folder_name to either local data or s3 stored data.
The file exixts in dish-devex-sdk -> devex_sdk -> tests-> commons.py
In our case we default to run these tests in the GitHub runner so we point to an s3 bucket.
```

the _pytest_ command must be within the same directory that the ___tests___ directory is located.  Once run, _pytest_ will generate output on the test.
## Test Building _devex_sdk_ With your Sub-Pacakge
It is time for a test build!  If you've followed the steps above, and your unit tests are all passing, then it's time to test-build _devex_sdk_ with your sub-package on your local machine.  This involves the following steps:

1. [Uninstall _devex_sdk_ from your pip package manager](#uninstall-devex_sdk-from-local-host)
2. [Compile a new .whl file including your sub-package](#build-whl-file)
3. [Install the new wheel file using pip](#install-new-whl-file)
4. [Test the features of your sub-package](#test-the-sub-package)

### Uninstall _devex_sdk_ from Local Host
Issue the following command in your terminal to remove the existing install of _devex_sdk_:
```console
 pip uninstall devex_sdk
```
### Build _.whl_ File
Navigate to the root of the _devex_sdk_ directory you have been working in on your local host.  Then issue the following command:
```console
  python setup.py bdist_wheel --version <VERSION_NUMBER>
```
This will generate the .whl file in the _dist_ directory at the root of the _devex_sdk_ file structure.

**NOTE**: the ***<VERSION_NUMBER>*** only effects your local build.  You can use any version number you like.  This can be helpful in testing prior to submitting a pull request.  Alternatively, you can eclude the ***--version <VERSION_NUMBER>*** flag and the .whl file name will output as ***devex_sdk-_VERSION_PLACEHOLDER_-py3-none-any.whl***

### Install New _.whl_ File
Next, from the same directory, execute the following command:
```console
  pip install /dist/*.whl
```
**Note:** in Windows, you will need to hit ___tab___ prior to executing the above command, this will autocomplete the name of the _.whl_ file. 

### Test the Sub-Package
Now navigate to your home directory to get out of the _devex_sdk_ folder, this will ensure that you are testing _devex_sdk_ off of the pip installed version, not the _devex_sdk_ directory:
```console
 cd ~
```
Now, enter a Python Environment and test your sub-package.  Try various levels of imports, test all the features, and ensure everything is behaving as it should.  For example, the _cricles_ sub-packge would be tested as follows
```console
>>> from devex_sdk import circles as ci
>>> mycircle = ci.Circle(2, "red")
>>> mycircle.radius
2
>>> mycircle.color
'red'
>>> ci.describe(mycircle)
This is a red circle with a radius of 2.
```
If everything in your algorithm is functioning as expected, then it's time to submit a pull request to have your code included in the next release of _devex_sdk_!

## README.md File Requirements

Each subpackage contributed to *devex_sdk* must have a README.md file included.  This tells other users how to successfully use your functions, the use cases for each function, and the expected outputs.  The README.md files should be included in the following location:

```console
> dish-devex-sdk
    > devex_sdk
        __init__.py
        > circles
            __init__.py
            CirclesClass.py
-->         README.md
        > [OtherPackages]
```
The minimum topics for inclusion in the README file are as follows:

1. Detailed description of each input
2. Detailed description of the expected output
3. An example call for each function you are contributing

## Submitting a Pull Request
Once all of the above steps are completed, your unit tests are all passing, and you are able to successfully build *devex_sdk* on your local machine then commit and push your branch.  It's now time to [submit a pull request](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/working-with-your-remote-repository-on-github-or-github-enterprise/creating-an-issue-or-pull-request#creating-a-pull-request).
