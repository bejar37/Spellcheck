'''A trie node. Represents a 'state' in the dictionary, from which different
words can be built. For a technical discussion, see:
        http://www.aclweb.org/anthology-new/J/J00/J00-1002.pdf

   Much of the code in this file was inspired by Steve Hanov, where he
   discussed this general concept on his blog:
           http://stevehanov.ca/blog/index.php?id=119 '''
class TrieNode():

        def __init__(self, transition = None):
                #trans is the last key added to children
                self.trans = transition
                #last_child is the last child (value) added to children
                self.last_child = None
                #children contains the valid transitions and the states that 
                #those transitions lead to, as keys and values of the dict, 
                #respectively.
                self.children = {}
                #Whether this node marks the end of a valid word.
                self.word = 0

        def __eq__(self, other):
                if self.__class__ == other.__class__:
                        return str(self) == str(other)
                return False

        def __hash__(self):
                return self.__str__().__hash__()

        '''The string representation of the node depends on the id of the 
        children that it leads to. Since we are assuming a sorted dictionary
        list, the string representation will never be consulted unless we
        can be sure that no more children will be added to the dictionary.'''
        def __str__(self):
                s = [str(self.word)]
                if self.children.keys():
                        y = [k for k in sorted(self.children.keys())]
                        s = [str(id(self.children[k])) for k in y]
                        s.append(str(self.word))

                return ''.join(s)

        '''Inserts a child node on the transition trans'''
        def insert_child(self, trans):
                child = TrieNode(trans) 
                self.children[trans] = child
                self.last_child = child
                self.trans = trans
                return child
        
        '''Recursive procedure which inserts a child on the transition from
        the beginning of the suffix, and then calls insert_child on the child
        that has just been added without the first character in the string.'''
        def insert_suffix(self, suffix):

                if len(suffix) == 0:
                        self.word = 1
                        return
                new = self.insert_child(suffix[0])
                new.insert_suffix(suffix[1:])

        '''Returns the last common prefix of the MA-FSA that contains the
        exact sequence of characters. For example, 'Abel' and 'Abel's' would
        have the common prefix of the states corresponding to the string 
        '^Abel'.'''
        def common_prefix(self, word, pre_len = 0):

                child = self.last_child

                if len(word) == 0 or self.trans != word[0] or child is None:
                        return self, pre_len

                pre_len += 1

                return child.common_prefix(word[1:], pre_len)

'''Checks if the descendant nodes of the current node reside within the 
   register. If they do, replace the children nodes with the nodes in the
   register, maximizing memory efficiency.'''
def replace_or_register(reg, node):

        repl = None

        if node.last_child:
                replace_or_register(reg, node.last_child)

        repl = reg.get(str(node.last_child))

        if repl:
                node.last_child = repl
                node.children[node.trans] = repl
        else:
                reg[str(node)] = node


