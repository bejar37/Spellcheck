#!/usr/bin/python

import sys
import trie
import checker

'''Function takes a list of words and builds an MA-FSA from the list,
   as long as the list is in alphabetical order. If the list isn't
   in alpha order, the algorithm will create a trie tree, which will
   be less space efficient but still usable. 

   ARGS: sort_dict - name of a file containing the word list to build
   the dictionary from. 

   Returns: The root node for the MA-FSA or Trie.
   This algorithm was taken from:
           http://www.aclweb.org/anthology-new/J/J00/J00-1002.pdf '''
def make_dawg(sort_dict):

        try:
                w_list = open(sort_dict, 'r')
        except IOError:
                print "Could not open file %s: run with valid input"%(sort_dict)
                sys.exit(0)

        root = trie.TrieNode()
        reg = {}

        for word in w_list:
                word = word.rstrip('\n')
                prefix, p_len = root.common_prefix(word)
                if prefix.last_child:
                        trie.replace_or_register(reg, prefix)
                prefix.insert_suffix(word[p_len:])

        w_list.close()
        trie.replace_or_register(reg, root)

        return root

''' Main program loop. Waits for user input, and spellchecks it. '''
def loop(root):

        while 1:
                try:
                        word = raw_input('> ')
                except EOFError:
                        print
                        sys.exit(0)
                word = word.strip('\n')
                checker.spellcheck(root, word)


if __name__=='__main__':
        if len(sys.argv) < 2:
                print "Usage: gen_mafsa sorted_dictionary"
                sys.exit(0)
        root = make_dawg(sys.argv[1])
        loop(root)

