from setuptools import setup
from Cython.Build import cythonize

setup( 
      ext_modules=cythonize(['../config/variable_tree_config.pyx',
                             '../config/tokenization_config.pyx', 
                             '../io_tree/input_tree.pyx',
                             '../io_tree/output_tree.pyx',
                             '../parser/display_parser.pyx',
                             '../data_node/data_node.pyx',
                             '../parser/get_parser.pyx',
                             '../parser/parser.pyx'
                             ])
    )
