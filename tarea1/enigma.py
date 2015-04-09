# -*- coding:utf-8 -*

"""
###############################################################################
###############################################################################
    
    Author : Pierre-Victor Chaumier <pvchaumier@uc.cl>
    Date : 6/04/2015

    IIC3253 - Cryptography and security
    HOMEWORK N°1 - Enigma machine

###############################################################################
    
    DESCRIPTION :

    The goal of this homework is to reproduce the enigma machine in code.
   
    The implementation of the enigma machine uses the description that can be 
    found on the wikipedia website http://en.wikipedia.org/wiki/Enigma_machine

    The algorithm uses the following steps :
        1) plugboard
        2) disc 1
        3) disc 2
        4) disc 3
        5) reflector
        6) disc 3 backward
        7) disc 2 backward
        8) disc 1 backward
        9) rotation of the discs
        10) plugboard

    or as an horizontal timeline :

    input -> plugboard -> disc1 -> disc2 -> disc3 -> reflector -> disc3 backward
        -> disc2 backward -> disc1 backward -> plugboard -> output

###############################################################################

    PRECAUTION :

    /!\ run this program in python3, using python2 will generate errors when 
    opening the files to read them (no encoding option in pyhton2).

###############################################################################

    CHOICES AND ASUMPTIONS :

    In the implementation, we make several asumptions/choices:
        1) the discs turn by adding the number of rotation (if A -> C and 
           B -> Z... after the rotation, B -> D and C -> A ...)
        2) the punctuation signs are not interpreted and are deleted and won't
           be rendered.
        3) all the letters of the input are lower cases
        4) the disc1 turns after each letter, the disc2 turns each 26 letters
           and the disc3 turns after each 26*26 letters. I have read that some
           implementation of the machine add a turn to the second disc when the 
           third rotate but as I have seen a lot of sources not mentionning it, 
           I choose not to implemente it.

###############################################################################

    HOW TO USE :
    1) to test :
       - uncomment the unittest line
       - launch the program without any cli argument
       - command : python enigma.py

    2) to use :
       - comment the unittest line if it is not
       - launch the program with all the arguments as follow : 
           python enigma.py path_disco1 path_disco2 path_disco3 path_plugboard 
       - ex :
       python enigma.py disco1.txt disco2.txt disco3.txt patch_panel_ejemplo.txt 

    rq: in the assignment, it is said that the reflector is fixed and thus is 
        not one of the command line argument. To change it, one simply need to 
        change the path given to the function encrypt at the end of this file.

###############################################################################
###############################################################################
"""

import os
import json
import string
import unittest
import argparse

###############################################################################
##  Helpers
###############################################################################

def file_to_array(file_path):
    """
        Function that takes the path to a disc or reflector file, reads it 
        and return an array representing the disc or reflector
    """
    res_array = []
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as file_content:
            for line in file_content:
                res_array.append(int(line))
            return res_array
    else:
        print(file_path, 'file does not exist.')

def file_double_to_array(file_path):
    """
        Function that takes the path to a plugboard file, reads it and return an
        array representing the plugboard
    """
    res_array = []
    if os.path.isfile(file_path):
        with open(file_path, 'r', encoding='utf-8') as file_content:
            for line in file_content:
                res_array.append([int(el) for el in line.split(',')])
            return res_array
    else:
        print(file_path, 'file does not exist.')

def plain_to_number(plain_text):
    """
        During the whole algorithm, we are using numbers. 1 is A, 2 is B ... 26
        is Z. 
        The point of this function is to change plain text in an array of
        corresponding int.
    """
    alphabet = string.ascii_lowercase
    plain_as_numbers = []
    for letter in plain_text:
        # Every text that is not a letter in lower case will disappear as the
        # enigma machine does not interpret ponctuation or spaces
        if letter in alphabet:
            plain_as_numbers.append(alphabet.index(letter) + 1)
    return plain_as_numbers

def number_to_plain(plain_as_numbers):
    """
        Final step of the algorithm, now that we have worked with int, we will
        transform them back to letters
    """
    plain_text = ''
    alphabet = string.ascii_lowercase
    for integ in plain_as_numbers:
        plain_text += alphabet[integ - 1]
    return plain_text

def go_through_plugboard(plain_as_numbers, plugboard):
    """
        Function that passes a word through the plugboard
    """
    for position, letter_as_int in enumerate(plain_as_numbers):
        for couple in plugboard:
            if letter_as_int in couple:
                couple_index = (couple.index(letter_as_int) + 1) % 2
                plain_as_numbers[position] = couple[couple_index]

def go_through_disc(letter_as_int, disc, position_disc):
    """
        Transform the letter as if going through the disc in the right way
    """
    index = (letter_as_int - 1 - position_disc) % 26
    if (disc[index] + position_disc) % 26 == 0:
        return 26
    else:
        return (disc[index] + position_disc) % 26

def go_through_reflector(letter_as_int, reflector):
    """
        Returns the transformed letter once it has passed through the
        reflector
    """
    if letter_as_int <= 13:
        return reflector[letter_as_int - 1]
    else:
        return reflector.index(letter_as_int) + 1


def go_through_disc_backwards(letter_as_int, disc, position_disc):
    """
        Transform the letter as if going through the disc when returning
    """
    if (letter_as_int - position_disc) % 26 == 0:
        index = 26
    else:
        index = (letter_as_int - position_disc) % 26
    return (disc.index(index) + position_disc) % 26 + 1

def create_parser_cli():
    """
        Function to get the paths from command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("disc1")
    parser.add_argument("disc2")
    parser.add_argument("disc3")
    parser.add_argument("patch")
    return parser

###############################################################################
##  Main
###############################################################################

def encrypt(plain_text, disc_1_path, disc_2_path, disc_3_path,
            reflector_path, plugboard_path):
    plain_as_numbers = plain_to_number(plain_text)
    disc_1 = file_to_array(disc_1_path)
    disc_2 = file_to_array(disc_2_path)
    disc_3 = file_to_array(disc_3_path)
    reflector = file_to_array(reflector_path)
    plugboard = file_double_to_array(plugboard_path)
    result_in_number = []
    position_disc_1 = position_disc_2 = position_disc_3 = 0
    cipher_plain_as_numbers = []

    # Step 1 : plugboard
    go_through_plugboard(plain_as_numbers, plugboard)

    # Loop though the plain text
    for letter_as_int in plain_as_numbers:
        if letter_as_int != -1:
            # Step 2 : disc 1
            letter_as_int = go_through_disc(letter_as_int, disc_1, 
                                            position_disc_1)
            # Step 3 : disc 2
            letter_as_int = go_through_disc(letter_as_int, disc_2, 
                                            position_disc_2)
            # Step 4 : disc 3
            letter_as_int = go_through_disc(letter_as_int, disc_3,
                                            position_disc_3)
            # Step 5 : reflector
            letter_as_int = go_through_reflector(letter_as_int, reflector)
            # Step 6 : disc 3 backwards
            letter_as_int = go_through_disc_backwards(letter_as_int, disc_3,
                                                      position_disc_3)
            # Step 7 : disc 2 backwards
            letter_as_int = go_through_disc_backwards(letter_as_int, disc_2,
                                                      position_disc_2)
            # Step 8 : disc 1 backwards
            letter_as_int = go_through_disc_backwards(letter_as_int, disc_1,
                                                      position_disc_1)

            # Step 9 : change position of discs
            position_disc_1 += 1
            if position_disc_1 % 26 == 0:
                position_disc_2 += 1
            if position_disc_1 % (26*26) == 0:
                position_disc_3 += 1

        cipher_plain_as_numbers.append(letter_as_int)

    # Step 10 : plugboard back
    go_through_plugboard(cipher_plain_as_numbers, plugboard)

    return number_to_plain(cipher_plain_as_numbers)


###############################################################################
##  Tests
###############################################################################

class enigmaTestCase(unittest.TestCase):
    
    def test_file_to_array(self):
        A = [7, 15, 9, 19, 12, 1, 23, 4, 3, 24, 8, 25, 16, 22, 14, 6, 21, 18, 
            10, 13, 2, 11, 26, 20, 5, 17]
        self.assertEqual(file_to_array('disco1.txt'), A)

    def test_file_double_to_array(self):
        A = [[2, 5], [21, 13], [9, 3]]
        self.assertEqual(file_double_to_array('patch_panel_ejemplo.txt'), A)

    def test_plain_to_number(self):
        A = [1, 2, 3, 4, 26]
        self.assertEqual(plain_to_number('abcdz'), A)

    def test_number_to_plain(self):
        A = 'abcdz'
        self.assertEqual(number_to_plain([1, 2, 3, 4, 26]), A)

    def test_go_through_plugboard(self):
        A = [1, 5, 2, 9, 7]
        plugboard = file_double_to_array('patch_panel_ejemplo.txt')
        plain_as_numbers = [1, 2, 5, 3, 7]
        go_through_plugboard(plain_as_numbers, plugboard)
        self.assertEqual(plain_as_numbers, A)

    def test_go_through_disc(self):
        disc = [2, 4, 1, 3]
        position_disc = 0
        self.assertEqual(go_through_disc(1, disc, position_disc), 2)

    def test_go_through_disc_2(self):
        disc = [2, 4, 1, 3]
        position_disc = 1
        self.assertEqual(go_through_disc(2, disc, position_disc), 3)

    def test_go_through_disc_backwards(self):
        disc = [2, 4, 1, 3]
        position_disc = 1
        self.assertEqual(go_through_disc_backwards(3, disc, position_disc), 2)

    def test_go_through_disc_backwards_2(self):
        disc = [2, 4, 1, 3]
        position_disc = 1
        self.assertEqual(go_through_disc_backwards(2, disc, position_disc), 4)

    def test_go_through_reflector(self):
        reflector = file_to_array('reflector.txt')
        self.assertEqual(go_through_reflector(1, reflector), 15)

    def test_go_through_reflector_2(self):
        reflector = file_to_array('reflector.txt')
        self.assertEqual(go_through_reflector(18, reflector), 2)

    def test_encrypt(self):
        self.assertEqual(encrypt('a a', 'disco1.txt', 'disco2.txt', 
            'disco3.txt', 'reflector.txt', 'patch_panel_ejemplo.txt'), 'ub')

    def test_encrypt_2(self):
        text_to_encrypt = string.ascii_lowercase
        text_encrypted = encrypt(text_to_encrypt, 'disco1.txt', 'disco2.txt', 
            'disco3.txt', 'reflector.txt', 'patch_panel_ejemplo.txt')
        text_double_encrypted = encrypt(text_encrypted, 'disco1.txt', 
                    'disco2.txt', 'disco3.txt', 
                    'reflector.txt', 'patch_panel_ejemplo.txt')
        self.assertEqual(text_to_encrypt, text_double_encrypted)


if __name__ == '__main__':
    # To launch the tests, uncomment the following line and launch the program
    # without any argument
    # unittest.main()
    parser = create_parser_cli()
    args = parser.parse_args()
    plain_text = input('plaintext > ')
    cipher_text = encrypt(plain_text, args.disc1, args.disc2, args.disc3,
            'reflector.txt', args.patch)
    print('ciphertext >', cipher_text)









