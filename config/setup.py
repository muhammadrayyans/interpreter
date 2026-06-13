from setuptools import setup
from Cython.Build import cythonize

setup( 
      ext_modules=cythonize(['variable_tree_config.pyx', 'tokenization_config.pyx'])
    )
