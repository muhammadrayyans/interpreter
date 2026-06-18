from setuptools import setup
from Cython.Build import cythonize

setup( 
      ext_modules=cythonize(['../condition_tree/evaluator_node.pyx',
                             '../config/variable_tree_config.pyx',
                             '../config/tokenization_config.pyx', 
                             '../library/maths/calculation.pyx',
                             '../io_tree/display_parser.pyx',
                             '../io_tree/output_tree.pyx',
                             '../data_node/data_node.pyx',
                             '../io_tree/get_parser.pyx',
                             '../io_tree/input_tree.pyx',
                             '../parser/parser.pyx'
                             ])
    )
