# -*- coding:utf-8 -*

"""
    Author : Pierre-Victor Chaumier <pvchaumier@uc.cl>
    Date : 6/04/2015

    IIC3253 - Cryptography and security
    HOMEWORK N°1 - Enigma machine

    The goal of this homework is to reproduce the whole enigma machine in code.
"""

import os, json, unittest

###############################################################################
##  Helpers
###############################################################################

def disc_file_to_array(disc_path):
    """
        Function that takes the path to a disc file, reads it and return an
        array representing the disc
    """
    disc_array = []
    if os.path.isfile(disc_path):
        with open(disc_path, 'r', encoding='utf-8') as disc_file:
            for line in disc_file:
                disc_array.append(int(line))
            return disc_array
    else:
        print(disc_path, 'file does not exist.')

def plugboard_file_to_array(plugboard_path):
    """
        Function that takes the path to a plugboard file, reads it and return an
        array representing the plugboard
    """
    plugboard_array = []
    if os.path.isfile(plugboard_path):
        with open(plugboard_path, 'r', encoding='utf-8') as plugboard_file:
            for line in plugboard_file:
                plugboard_array.append([int(el) for el in line.split(',')])
            return plugboard_array
    else:
        print(plugboard_path, 'file does not exist.')

def reflector_file_to_array(reflector_path):
    """
        Function that takes the path to a disc file, reads it and return an
        array representing the disc
    """
    reflector_array = [0] * 26
    num_line = 1
    if os.path.isfile(reflector_path):
        with open(reflector_path, 'r', encoding='utf-8') as reflector_file:
            for line in reflector_file:
                el = int(line)
                reflector_array[num_line - 1] = el
                reflector_array[el - 1] = num_line
                num_line += 1
            return reflector_array
    else:
        print(reflector_path, 'file does not exist.')


###############################################################################
##  Main
###############################################################################


###############################################################################
##  Tests
###############################################################################

class enigmaTestCase(unittest.TestCase):
    
    def test_disc_file_to_array(self):
        A = [7, 15, 9, 19, 12, 1, 23, 4, 3, 24, 8, 25, 16, 22, 14, 6, 21, 18, 
            10, 13, 2, 11, 26, 20, 5, 17]
        self.assertEqual(disc_file_to_array('disco1.txt'), A)

    def test_plugboard_file_to_array(self):
        A = [[2, 5], [21, 13], [9, 3]]
        self.assertEqual(plugboard_file_to_array('patch_panel_ejemplo.txt'), A)

    def test_reflector_file_to_array(self):
        A = [[1, 15], [2, 18], [3, 14], [4, 26], [5, 24], [6, 16], [7, 25], 
             [8, 21], [9, 17], [10, 23], [11, 20], [12, 22], [13, 19]]
        self.assertEqual(reflector_file_to_array('reflector.txt'), A)

if __name__ == '__main__':
    for key, value in enumerate(reflector_file_to_array('reflector.txt')):
        print(key, value)
    # unittest.main()