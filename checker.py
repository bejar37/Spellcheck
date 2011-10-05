import utils

'''Builds the suggestions for the tree and returns the spellchecked word. 
   
   Args: the root of the current MA-FSA, the current part of the word to
   be checked, and the previous character in the word (to check for
   repetitions).

   Returns: If the previous character is part of a valid word, 
   appends cur to the response, and returns the response. Else returns None.'''
def _suggestion(root, word, prev_char = ''):

        possible = set(root.children.keys()) #The possible next characters
        response = None
        cur = ''

        if len(word) == 0:
                if root.word:
                        return []
                else:
                        return None


        while response == None:
                cur, offset = _next(possible, word, prev_char)
                if cur:
                        #Returns the response of cur to see if cur is
                        #part of a word
                        response = _suggestion(root.children[cur],
                                               word[offset:], cur)
                        possible.remove(cur)
                elif cur == '':
                        #If _next got to the end of input, check if word
                        if root.word:
                                return []
                        return None
                else:
                        #The previous character does not form part of a 
                        #valid word. Return None.
                        return cur

        response.append(cur)
        return response

'''Returns a suggestion from the set of possible next states, given the 
   previous character. If a character cannot be found, then the previous
   character does not form part of a dictionary word.
   Uses a greedy algorithm to consume the word. If the previous character
   and the beginning of the word are the same, runs until a new character 
   ocurrs, and then starts trying to come up with a new character.
   This is the source of a bug (06/15/2011). If there is a sequence of three
   consecutive vowels, the algorithm will only be able to handle two of them, 
   the first and the last vowel. This means that some good spelling corrections
   to words aren't made.
   
   Args: possible - set of possible next states given the previous character
         word - rest of the word to be spellchecked
         prev - previous character in the word
         
   Returns: offset - position in the word after which the next character
            should be inserted.
            Also, either None, a character, or the empty string. 
            Returns None if no possible character can be found, and
            the the end of the word input is not a run of the same letters.
            Returns a character if a next possible character was found.
            Returns the empty string if no next character was found, but 
            the end of the input had a single run of the same letter.'''

def _next(possible, word, prev):

        offset = 0

        vowels = {'A', 'E', 'I', 'O', 'U', 'a', 'e', 'i', 'o', 'u'}


        cur = word[offset]
        temp = utils.change_case(cur)


        if prev == cur or prev == temp:
                #Run to the end of the input
                offset = rep_chars(word, offset)

        while 1:
                cur = word[offset]
                temp = utils.change_case(cur)

                if cur in possible:
                        offset += 1
                        return cur, offset

                if temp in possible:
                        offset += 1
                        return temp, offset

                if cur in vowels:
                        pos_v = vowels.intersection(possible)
                        if pos_v:
                                offset += 1
                                return pos_v.pop(), offset
                if offset < 1:
                        break
                offset -= 1

        char, offset = check_final_run(word, prev, offset)
        return char, offset

''' Finds the offset of the first character different from the initial 
    character. Returns the index of the last character if there are no more
    different characters in the word.'''
def rep_chars(word, offset):
        rep = word[0]
        other_case = utils.change_case(word[0])

        for char in word:
                if char != rep and char != other_case and \
                len(word[offset:]) != 0:
                        return offset
                offset += 1


        return offset - 1

'''Checks if the current characters are just a set of repetitions of the same
   character. If so, returns the empty string, and
   the offset of the last character. If not, returns None.'''
def check_final_run(word, prev_char, offset):

        for char in word:
                if char != prev_char:
                        return None, offset
                offset += 1
        return '', offset

'''Collects the results from _suggestion, and reverses them to create
   the spelling correction. Prints the suggestion if one is received, 
   otherwise prints NO SUGGESTION'''
def spellcheck(root, word):
        msg = _suggestion(root, word, '')
        if msg == None:
                print "NO SUGGESTION"
                return False
        else: 
                msg.reverse()
                print ''.join(msg)
                return True
