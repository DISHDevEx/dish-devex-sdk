from setuptools import find_packages, setup

setup(
    name='msspackages',
    version='0.0.4',    
    description='MSS team packages for distributed use',
    url='https://git-codecommit.us-west-2.amazonaws.com/v1/repos/msspackages',
    
    author= 'Praveen Mada, Hamza Khokhar, Pierce Lovesee',
    author_email='praveen.mada@dish.com, hamza.khokhar@dish.com, pierce.lovesee@dish.com',
    license='',
    packages=find_packages(include=['msspackages', 'msspackages.extras', 'msspackages.circles',
                                    'msspackages.parity','msspackages.bucketization', 'msspackages.update_cwd','msspackages.data_ingestion','msspackages.data_ingestion.container_insights_schema']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: MSS Team',
    ],
)