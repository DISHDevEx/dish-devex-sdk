"""
Build the wheel file for the library devex_sdk.
"""

from setuptools import find_packages, setup
from sys import argv

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Pierce, working with command line arguments

# total arguments
def total_args():
    n = len(sys.argv)
    print("Total arguments passed:", n)


# Arguments passed
def list_args():
    print("\nName of Python script:", sys.argv[0])

    print("\nArguments passed:", end=" ")
    for i in range(1, n):
        print(sys.argv[i], end=" ")


# def get_version(rel_path):
#     for line in read(rel_path).splitlines():
#         if line.startswith('__version__'):
#             delim = '"' if '"' in line else "'"
#             return line.split(delim)[1]
#     else if ('{{VERSION_PLACEHOLDER}}')
#     else:
#         raise RuntimeError("Unable to find version string.")

# Pierce additions
total_args()
list_args()

# End Pierce additions

setup(
    name='devex_sdk',
    version='{{VERSION_PLACEHOLDER}}',
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
