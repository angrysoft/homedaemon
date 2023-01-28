from setuptools import setup, find_packages
from homed import __version__


setup(
    name='HomeDaemon',
    version=__version__,
    packages=find_packages(),
    url='https://bitbucket.org/angrysoft/homedaemon',
    license='Apache 2.0',
    author='AngrySoft',
    author_email='sebastian.zwierzchowski@gmail.com',
    description='',
    scripts=['homed.py'],
    requires=["pyiot"],
    data_files=[('/usr/lib/systemd/system', ['homed.service'])],
)
