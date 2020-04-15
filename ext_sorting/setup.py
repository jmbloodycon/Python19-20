from setuptools import setup, find_packages
from os.path import join, dirname

setup(name='External sorting',
      description="External merge for large files",
      version='1.0',
      author="Elizaveta Kokorina",
      author_email="ekell11lle@gmail.com",
      packages=find_packages(),
      long_description=open(join(dirname(__file__), 'README.md')).read(),
      entry_points={
        'console_scripts': ['external_sorting = external_sort.ext_sorting:start']
      }
)
