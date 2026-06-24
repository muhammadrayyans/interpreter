from setuptools import setup
from Cython.Build import cythonize
import os

setup( 
      ext_modules=cythonize(['../data_node/type_conversion/integer.pyx',
                             '../condition_tree/condition_parser.pyx',
                             '../condition_tree/condition_tree.pyx',
                             '../config/variable_tree_config.pyx',
                             '../config/tokenization_config.pyx', 
                             '../library/maths/calculation.pyx',
                             '../utils/condition_extractor.pyx',
                             '../io_tree/display_parser.pyx',
                             '../utils/condition_scope.pyx',
                             '../utils/evaluator_node.pyx',
                             '../io_tree/output_tree.pyx',
                             '../data_node/data_node.pyx',
                             '../io_tree/get_parser.pyx',
                             '../io_tree/input_tree.pyx',
                             '../parser/env_parser.pyx',
                             '../parser/parser.pyx'
                             ])
    )
