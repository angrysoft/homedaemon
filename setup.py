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
wwwStatic = get_files('src/static')
wwwStaticRf = get_files('src/static/rfpilot')
wwwStaticTv = get_files('src/static/tvpilot')
wwwTemp = get_files('src/templates')

setup(name='SmartHouse',
      version='0.5',
      description='House Automatization',
      url='https://bitbucket.org/angrysoft/Smarthouse',
      author='Sebastian Zwierzchowski',
      author_email='sebastian.zwierzchowski@gmail.com',
      license='GPL2',
      package_dir={'house': 'src/house'},
      packages=['house'],
      # py_modules=['src/house.bravia'],
      data_files=[('/etc/smarthouse', confFile),
                  ('/var/www/smarthouse', ['src/SmartHouse.py']),
                  ('/var/www/smarthouse/static', wwwStatic),
                  ('/var/www/smarthouse/static/rfpilot', wwwStaticRf),
                  ('/var/www/smarthouse/static/tvpilot', wwwStaticTv),
                  ('/var/www/smarthouse/templates', wwwTemp),
                  ('/usr/lib/systemd/system', ['housed.service'])],
      scripts=['src/housed.py'],
      requires=["flask", "pyserial"])
