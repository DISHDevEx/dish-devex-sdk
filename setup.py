"""
Build the wheel file for the library devex_sdk.
"""

from setuptools import find_packages, setup
import sys

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


def get_version():
    """
    Checks commandline arguments for a user specified Version number.
    If the --version flag is not given at run time, then the version number is defaulted to
    {{VERSION_PLACEHOLDER}}, which will later be replaced with a git tag when performing
    version releases.

    Returns
    -------
    when the bdist_wheel command is given a version flag and version number, such as:

    --version 1.x.x

    the version of the built whl file will include the given version number, such as:

    devex_sdk-1.x.x-py3-none-any.whl


    Error Handling
    --------------
    If the --version flag is given, but no version number is supplied, such as:

    --version

    then an IndexError will be thrown and the build will exit with exit status 1.

    """
    version = '{{VERSION_PLACEHOLDER}}'
    if "--version" in sys.argv:
        try:
            version = sys.argv[3]
            sys.argv.remove(sys.argv[3])
        except IndexError as e:
            print("error:  " + str(e))
            print("supply a version number i.e. --version 1.x.x")
            exit(1)
        sys.argv.remove("--version")
    return version


version_var = str(get_version())


setup(
    name='devex_sdk',
    version=version_var,
    description='Dish DevEx open source SDK',
    url='https://git-codecommit.us-west-2.amazonaws.com/v1/repos/devex_sdk',
    author_email='devex@dish.com',
    license='Dish Wireless',
    packages=find_packages(
        include=['devex_sdk',
                 'devex_sdk.extras',
                 'devex_sdk.circles',
                 'devex_sdk.parity',
                 'devex_sdk.bucketization',
                 'devex_sdk.update_cwd',
                 'devex_sdk.data_ingestion',
                 'devex_sdk.data_ingestion.container_insights_schema',
                 'devex_sdk.project_inital_setup',
                 'devex_sdk.feature_engine.eks_feature_store',
                 'devex_sdk.feature_engine',
                 'devex_sdk.data_ingestion.gz_connector',
                 'devex_sdk.utilities'
        ]
    ),
    include_package_data=True,
    install_requires=[
        'pyspark',
        'pandas',
        'numpy',
        'tqdm',
        'pyspark',
        'configparser',
        'dask',
        'boto3',
        'fastparquet',
        'pyarrow',
        ],
    long_description=long_description,
    long_description_content_type='text/markdown'
    )
