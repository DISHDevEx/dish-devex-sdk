"""
Build the wheel file for the library devex_sdk.
"""

from setuptools import find_packages, setup


from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = 'devex_sdk',
    version = 'v1.0.0',
    description = 'Dish DevEx open source SDK',
    url = 'https://git-codecommit.us-west-2.amazonaws.com/v1/repos/devex_sdk',
    author_email = 'devex@dish.com',
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
    install_requires = [
        'pyspark',
        'pandas',
        'numpy',
        'tqdm',
        'pyspark',
        'configparser',
        'dask',
        ],
    long_description=long_description,
    long_description_content_type='text/markdown'
    )
