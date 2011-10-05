#!/usr/bin/python

import utils
import random
import sys

VOWEL = 1
CAPITALIZATION = 2
REPETITION = 3

vowels = ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
def gen_error(word):

        new_word = [] 
        for char in word:
                if not char.isalpha():
                        new_word.append(char)
                        continue
                to_do = random.randint(1, 4)

                if to_do == VOWEL and utils.is_vowel(char):
                        new_word.append(random.choice(vowels))
                elif to_do == CAPITALIZATION:
                        new_word.append(utils.change_case(char))
                elif to_do == REPETITION:
                        while 1:
                                new_word.append(char)
                                if random.randint(0, 1):
                                        break
                else:
                        new_word.append(char)
        return ''.join(new_word)

def print_mispellings(f):
        f = open(f, "r")

        for line in f:
                word = line.rstrip('\n')
                print gen_error(word)

        f.close()

if __name__ == '__main__':
        if len(sys.argv) < 2:
                print "Usage: mispelling.py word_dictionary"
                sys.exit(0)

        print_mispellings(sys.argv[1])

