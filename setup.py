from setuptools import setup

setup(
  name='pickleable',
  packages=['pickleable'],
  version='0.1.2',
  author='Hampus Hallman',
  author_email='me@hampushallman.com',
  url='https://github.com/Reddan/pickleable',
  license='MIT',
  install_requires=[
    'checkpointer',
  ],
  python_requires='~=3.5',
)
