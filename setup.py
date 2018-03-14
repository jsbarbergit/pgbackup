from setuptools import setup, find_packages

# Load existing README.rst for long description
with open('README.rst', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='pgbackup',
    version='0.1.0',
    description='Database backups locallly or to AWS S3',
    long_description=readme,
    author='John Barber',
    author_email='jsbarber@gmail.com',
    install_requires=['boto3'],
    # Will recursively look through given dir for __init__.py to indicate req'd pkgs
    packages=find_packages('src'),
    package_dir={'':'src'},
    entry_points={
        'console_scripts': [
            'pgbackup = pgbackup.cli:main',
            ]
    }
)
