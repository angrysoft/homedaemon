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
wwwStatic = get_files('www/static')
wwwStaticRf = get_files('www/static/rfpilot')
wwwStaticTv = get_files('www/static/tvpilot')
wwwStaticLed = get_files('www/static/ledpilot')
wwwTemp = get_files('www/templates')

setup(name='AngryHome',
      version='0.5',
      description='Home Automatization',
      url='https://bitbucket.org/angrysoft/angryhome',
      author='Sebastian Zwierzchowski',
      author_email='sebastian.zwierzchowski@gmail.com',
      license='GPL2',
      package_dir={'': 'lib'},
      packages=['house'],
      data_files=[('/etc/angryhome', confFile),
                  ('/etc/angryhome/events', get_files('events')),
                  ('/var/www/angryhome', ['www/AngryHome.py']),
                  ('/var/www/angryhome/static', wwwStatic),
                  ('/var/www/angryhome/static/rfpilot', wwwStaticRf),
                  ('/var/www/angryhome/static/tvpilot', wwwStaticTv),
                  ('/var/www/angryhome/static/ledpilot', wwwStaticLed),
                  ('/var/www/angryhome/templates', wwwTemp),
                  ('/usr/lib/systemd/system', ['homed.service'])],
      scripts=['scripts/housed.py'],
      requires=["flask", "pyserial"])
