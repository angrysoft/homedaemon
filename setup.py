from setuptools import setup, find_packages
from glob import glob
import os
from homed import __version__


def get_files(name):
    for dirname, dirnames, filenames in os.walk(name):
        if dirname == name:
            return [os.path.join(dirname, f) for f in filenames]
        else:
            continue


scenes = glob('scenes/*.py')

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
    requires=["flask", "pyserial", "pyxiaomi", 'pycouchdb'],
    data_files=[('/etc/angryhome/scenes', scenes),
                ('/usr/lib/systemd/system', ['homed.service'])],
)
