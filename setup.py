from distutils.core import setup
from glob import glob

confFile = glob('files/*.json')
wwwStatic = glob('src/static/*css') + glob('src/static/*.dart') + glob('src/static/*.dart.js')
wwwTemp = glob('src/templates/*.html')


setup(name='SmartHouse',
    version='0.4',
    description='Home Automatization',
    url='https://bitbucket.org/angrysoft/SmartHome',
    author='Sebastian Zwierzchowski',
    author_email='sebastian.zwierzchowski@gmail.com',
    license='GPL2',
    data_files=[('/etc/marthome', confFile),
                ('/var/www/smarthome/static', wwwStatic),
                ('/var/www/smarthome/templates', wwwTemp),
                ('/var/www/smarthome', 'src/SmartHome.py')
                ('/usr/lib/systemd/system', 'housed.service')],
    scripts=['src/housed.py'],
    install_requires=["flask", "pyserial"]
    )
