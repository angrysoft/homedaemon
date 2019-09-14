from setuptools import setup, find_packages
from glob import glob
import os


def get_files(name):
    for dirname, dirnames, filenames in os.walk(name):
        if dirname == name:
            return [os.path.join(dirname, f) for f in filenames]
        else:
            continue


confFile = glob('files/*.json')
scenes = glob('files/scenes/*.json')
wwwStatic = get_files('www/static')
wwwStaticDevs = get_files('www/static/devices')
wwwStaticTv = get_files('www/static/tvpilot')
wwwStaticLed = get_files('www/static/ledpilot')
wwwTemp = get_files('www/templates')

setup(
    name='AngryHome',
    version='0.9',
    packages=find_packages(),
    url='https://bitbucket.org/angrysoft/angryhome',
    license='Apache 2.0',
    author='AngrySoft',
    author_email='sebastian.zwierzchowski@gmail.com',
    description='',
    scripts=['homed.py'],
    requires=["flask", "pyserial", "pyxiaomi", "websockets", 'pycouchdb'],
    data_files=[('/etc/angryhome', confFile),
                ('/etc/angryhome/scenes', scenes),
                ('/var/www/angryhome', ['www/AngryHome.py']),
                ('/var/www/angryhome/static', wwwStatic),
                ('/var/www/angryhome/static/devices', wwwStaticDevs),
                ('/var/www/angryhome/static/tvpilot', wwwStaticTv),
                ('/var/www/angryhome/static/ledpilot', wwwStaticLed),
                ('/var/www/angryhome/templates', wwwTemp),
                ('/usr/lib/systemd/system', ['homed.service'])],
)
