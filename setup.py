from distutils.core import setup
from glob import glob
import os


def get_files(name):
    for dirname, dirnames, filenames in os.walk(name):
        if dirname == name:
            return [os.path.join(dirname, f) for f in filenames]
        else:
            continue


confFile = glob('files/*.json')
wwwStatic = get_files('www/static')
wwwStaticRf = get_files('www/static/rfpilot')
wwwStaticTv = get_files('www/static/tvpilot')
wwwStaticLed = get_files('www/static/ledpilot')
wwwTemp = get_files('www/templates')

setup(name='SmartHouse',
      version='0.5',
      description='House Automatization',
      url='https://bitbucket.org/angrysoft/Smarthouse',
      author='Sebastian Zwierzchowski',
      author_email='sebastian.zwierzchowski@gmail.com',
      license='GPL2',
      package_dir={'': 'lib'},
      packages=['house'],
      data_files=[('/etc/smarthouse', confFile),
                  ('/etc/smarthouse/events', get_files('events')),
                  ('/var/www/smarthouse', ['www/SmartHouse.py']),
                  ('/var/www/smarthouse/static', wwwStatic),
                  ('/var/www/smarthouse/static/rfpilot', wwwStaticRf),
                  ('/var/www/smarthouse/static/tvpilot', wwwStaticTv),
                  ('/var/www/smarthouse/static/ledpilot', wwwStaticLed),
                  ('/var/www/smarthouse/templates', wwwTemp),
                  ('/usr/lib/systemd/system', ['housed.service'])],
      scripts=['scripts/housed.py'],
      requires=["flask", "pyserial"])
