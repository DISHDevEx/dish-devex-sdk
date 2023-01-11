"""
Build the wheel file for the library MSSPackages.
"""

from setuptools import find_packages, setup

setup(
    name = 'msspackages',
    version = '0.0.7',
    description = 'MSS team packages for distributed use',
    url = 'https://git-codecommit.us-west-2.amazonaws.com/v1/repos/msspackages',
    author = 'Hamza Khokhar, Praveen Mada, Pierce Lovesee',
    author_email = 'hamza.khokhar@dish.com, '
                 + 'praveen.mada@dish.com, '
                 + 'pierce.lovesee@dish.com ',
    license='Dish Wireless',
    packages=find_packages(
        include=['msspackages',
                 'msspackages.extras',
                 'msspackages.circles',
                 'msspackages.parity',
                 'msspackages.bucketization',
                 'msspackages.update_cwd',
                 'msspackages.data_ingestion',
                 'msspackages.data_ingestion.container_insights_schema',
                 'msspackages.project_inital_setup',
                 'msspackages.feature_engine.eks_feature_store',
                 'msspackages.feature_engine',
                 ]),
    include_package_data=True,
#     entry_points = {
#         'console_scripts':
#             ['msspackages=msspackages.project_inital_setu:setup_runner'],}
#     scripts=['msspackages/project_inital_setup/understanding_eks_setup.py'],
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
