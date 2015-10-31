from distutils.core import setup

setup(name='SmartHome',
      version='0.2',
      description='Home Automatization',
      url='https://bitbucket.org/angrysoft/SmartHome',
      author='Sebastian Zwierzchwoski',
      author_email='sebastian.zwierzchowski@gmail.com',
      license='GPL2',
      packages_dir=['src'],
      scripts=['src'],
      install_requires=["flask", "pyserial"]
      )