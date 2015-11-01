from distutils.core import setup

setup(name='SmartHome',
    version='0.4',
    description='Home Automatization',
    url='https://bitbucket.org/angrysoft/SmartHome',
    author='Sebastian Zwierzchwoski',
    author_email='sebastian.zwierzchowski@gmail.com',
    license='GPL2',
    data_files=[('/etc/SmartHome', ['files/colors.json',
                                    'files/commands.json',
                                    'files/IR.json',
                                    'files/rf433.json',
                                    'files/sensors.json']),
                ('/usr/share/SmartHome/static', ['src/static/styles.css', 'src/static/funct.js'])],
    scripts=['src/server.py'],
    install_requires=["flask", "pyserial"]
    )