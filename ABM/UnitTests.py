#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 14:06:54 2022

@author: mmp
"""

import unittest
from Functions import *

# class UnitTests(unittest.TestCase):

#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')

#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())

#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)


class FunctionTests(unittest.TestCase):
    
    def test_normalDistNP(self):
        arr = []
        sum_arr = 0
        for i in range(30):
            arr.append(normalDistNP(30))
        
        for j in arr:
            sum_arr += len(j)
        
        self.assertEqual(sum_arr,900)


if __name__ == '__main__':
    unittest.main()
