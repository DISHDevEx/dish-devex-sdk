"""
Build the wheel file for the library devex_sdk.
"""

from setuptools import find_packages, setup

setup(
    name = 'devex_sdk',
    version = '0.0.8',
    description = 'MSS team packages for distributed use',
    url = 'https://git-codecommit.us-west-2.amazonaws.com/v1/repos/devex_sdk',
    author = 'Hamza Khokhar, Praveen Mada, Pierce Lovesee',
    author_email = 'hamza.khokhar@dish.com, '
                 + 'praveen.mada@dish.com, '
                 + 'pierce.lovesee@dish.com ',
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
                 ]),
    include_package_data=True,
#     entry_points = {
#         'console_scripts':
#             ['devex_sdk=devex_sdk.project_inital_setu:setup_runner'],}
#     scripts=['devex_sdk/project_inital_setup/understanding_eks_setup.py'],
    install_requires = [
        'pyspark',
        'pandas',
        'numpy',
        'tqdm',
        'pyspark',
        'configparser',
        'dask',
        ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Dish Wireless',
        ],
    )
