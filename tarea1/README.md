# IIC3253 - Cryptography and security
## HOMEWORK N°1 - Enigma machine

### DESCRIPTION :

The goal of this homework is to reproduce the **enigma machine** in code.

The implementation of the enigma machine uses the description that can be found on the [wikipedia website](http://en.wikipedia.org/wiki/Enigma_machine)

The algorithm uses the following steps :
- plugboard
- disc 1
- disc 2
- disc 3
- reflector
- disc 3 backward
- disc 2 backward
- disc 1 backward
- rotation of the discs
- plugboard

or as an horizontal timeline :

input -> plugboard -> disc1 -> disc2 -> disc3 -> reflector -> disc3 backward -> disc2 backward -> disc1 backward -> plugboard -> output

### PRECAUTION :

/!\ run this program in python3, using python2 will generate errors when opening the files to read them (no encoding option in pyhton2).

### CHOICES AND ASUMPTIONS :

In the implementation, we make several asumptions/choices:
- the discs turn by adding the number of rotation (if A -> C and B -> Z... after the rotation, B -> D and C -> A ..)
- the punctuation signs are not interpreted and are deleted and won'tbe rendered.
- all the letters of the input are lower cases
- the disc1 turns after each letter, the disc2 turns each 26 letters and the disc3 turns after each 26*26 letters. I have read that some implementation of the machine add a turn to the second disc when the  third rotate but as I have seen a lot of sources not mentionning it, I choose not to implemente it.

### HOW TO USE :
- to test :
  * uncomment the unittest line
  * launch the program without any cli argument
  * command : python enigma.py

- to use :
  * comment the unittest line if it is not
  * launch the program with all the arguments as follow : 
    python enigma.py path_disco1 path_disco2 path_disco3 path_plugboard 
  * ex :
    python enigma.py disco1.txt disco2.txt disco3.txt patch_panel_ejemplo.txt 

rq: in the assignment, it is said that the reflector is fixed and thus is not one of the command line argument. To change it, one simply need to change the path given to the function encrypt at the end of this file.