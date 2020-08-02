from setuptools import setup, find_packages
from homed import __version__


setup(
    name='AngryHome',
    version=__version__,
    packages=find_packages(),
    url='https://bitbucket.org/angrysoft/angryhome',
    license='Apache 2.0',
    author='AngrySoft',
    author_email='sebastian.zwierzchowski@gmail.com',
    description='',
    scripts=['homed.py'],
    requires=["flask", "pyserial", "pyiot", 'pycouchdb'],
    data_files=[('/usr/lib/systemd/system', ['homed.service'])],
)
