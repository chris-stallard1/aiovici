from setuptools import setup
setup(
  name = 'aiovici',
  packages = ['aiovici'],
  version = '0.1',
  license='MIT',
  description = 'A library to control Vici Multipos Selector & Switch valves, with asyncio integration',
  author = 'Christopher Stallard',
  author_email = 'christopher.stallard1@gmail.com',
  url = 'https://github.com/chris-stallard1/aiovici',
  keywords = ['vici'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: MIT License',
    'Framework :: AsyncIO',
    'Programming Language :: Python :: 3'
  ],
)
