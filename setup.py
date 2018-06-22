from distutils.core import setup
from glob import glob

confFile = glob('files/*.json')
wwwStatic = glob('src/static/*css') + glob('src/static/*.dart') + glob('src/static/*.dart.js')
wwwTemp = glob('src/templates/*.html')


setup(name='SmartHouse',
      version='0.4',
      description='House Automatization',
      url='https://bitbucket.org/angrysoft/Smarthouse',
      author='Sebastian Zwierzchowski',
      author_email='sebastian.zwierzchowski@gmail.com',
      license='GPL2',
      package_dir={'house': 'src/house'},
      packages=['house'],
      data_files=[('/etc/smarthouse', confFile),
                  ('/var/www/smarthouse', 'src/SmartHouse.py'),
                  ('/var/www/smarthouse/static', wwwStatic),
                  ('/var/www/smarthouse/templates', wwwTemp),
                  ('/usr/lib/systemd/system', 'housed.service')],
      scripts=['src/housed.py'],
      requires=["flask", "pyserial"]
    )
