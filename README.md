# MSS Packages

## __How to Use__

### __Cloning the Repository__
The process for cloning the repository is different depending on if the package is hosted on AWS CodeCommit or the Dish on-premise GitLab.  Instructions for both processes have been provided below:

#### __AWS CodeCommit (Current Platform)__
1. In your browser, navigate to your list of AWS accounts
2. Search for ___aws-5g.dp.mss.data-science.dev___ and press the arrow to view all available roles
![Expand to See Roles](./images/arrow.PNG?raw=true "Expand to see roles")
3. To the right of your desired role, click ___Command line or programmatic access___
![CLI Programmatic Access ](./images/cli_progromatic_access.PNG?raw=true "CLI Access")
4. You will now be presented with something similar to the following screen, you will only need to focus on the three values presented in ___Option 3___ - AWS Access Key Id, AWS Secret access key, and AWS session token:
![AWS CLI Credentials](./images/Credentials.PNG?raw=true "Credentials")
5. Next, open a terminal and issue the following commands:
```console
$ pip install git-remote-codecommit
$ aws configure
```
6. Copy the value for ___AWS Access Key Id___ from your CLI credentials on AWS and paste it in the terminal when prompted for ___AWS Access Key ID:___; press enter
7. The next prompt will be for ***AWS Secret Access Key***.  Copy and paste the value from your AWS Credentials for ***AWS Secret access key*** and press enter
8. The next prompt, ***Default region name***, set to "***us-west-2***" and for the following prompt, ***Default output format***, leave as default by pressing enter
9. Next, issue the following command in the terminal, replacing ___(AWS-SESSION-TOKEN)___ with the copy/pasted value for ***AWS session token*** from your CLI Credentials on AWS; then press enter:
```console
$ aws configure set aws_session_token (AWS-SESSION-TOKEN)
```
10. You should now have CLI access to this AWS Account / Role for a period of time.  The credentials do periodically expire, so you will need to repeat this process from time-to-time
11. Now to clone the repo, on the AWS Account page, click on the ***aws-5g.dp.mss.data-science.dev*** to expand options and select ***Management console*** to enter the account
![Enter AWS Account](./images/Enter_account.PNG?raw=true "Enter MSS Dev account")
12. Next, using the search bar at the top of the Management console, search for ___CodeCommit___ and select the correct service from the list:
![Search for CodeCommit](./images/Search.PNG?raw=true "Search for CodeCommit")
13. Now, you will be presented with a list of repositories.  Locate the *msspackages* repository in the list.  Click the ***HTTPS (GRC)*** option on the right hand side in the ***Clone URL*** column; this copies the link to your clip board:
![Clone Link](./images/clone_link.PNG?raw=true "Clone Link")
14. Next, change your present working directory in your terminal to the location you keep your git repositories on your local machine.  Once you have navigated there, issue the following command, replacing ***(HTTPS(GRC)-LINK)*** with the pasted value from the previous step; press enter and the repository will clone
```console
$ git clone (HTTPS(GRC)-LINK)
```
#### __GitLab__
1. Navigate to your ***git*** directory on your local machine
2. Clone the repo
```console
$ git clone https://gitlab.global.dish.com/MSS/msspackages.git
```
### __Installing msspackages__
1. Navigate into the root _msspackages_ directory.
```console
$ cd msspackages
```
2. Run the following command to create the wheel file
 
```console
$ python setup.py bdist_wheel
```
3. Next, pip install the wheel file by running the following command, note that the _version_ will change depending upon the release:
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


