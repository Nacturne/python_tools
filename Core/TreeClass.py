__author__ = 'Nacturne'

import re


class WordNode(object):
    def __init__(self, label, parent, word, index):
        self.word = word
        self.label =label
        self.parent = parent
        self.index = index

    def isRoot(self):
        return False


class LabelNode(object):
    def __init__(self, label, parent, children, index):
        self.label = label
        self.children = children
        self.parent = parent
        self.index = index

    def isRoot(self):
        if self.parent:
            return False
        else:
            return True

    def num_subnodes(self):
        '''
        :return: the number of nodes in the tree rooted at this node. (this node is included)
        '''
        counter = 0
        temp = []

        temp.append(self)

        while len(temp) != 0:
            x = temp.pop(0)
            counter += 1
            if not(x.isLeaf()):
                for child in x.children:
                    temp.append(child)
        return counter

    def num_leaves(self):
        '''
        :return: the number of leaves in the tree rooted at this node. (this node is included)
        '''
        counter = 0
        temp = []

        temp.append(self)

        while len(temp) != 0:
            x = temp.pop(0)
            if x.isLeaf():
                counter += 1
            else:
                for child in x.children:
                    temp.append(child)
        return counter

    def num_phrases(self):
        '''
        :return: the number of phrases ocntained in the tree rooted at this node.
        '''
        return (self.num_subnodes() - self.num_leaves())

    def isLeaf(self):
        if type(self.children[0]) is WordNode:
            return True
        else:
            return False

    def wordNodes(self):
        '''
        :return: the list of all wordNodes in the tree rooted at this node, sorted by their order in the raw sentence
        '''
        list = []
        queue = [self]
        while(queue):
            node = queue.pop(0)
            if node.isLeaf():
                list.append(node.children[0])
            else:
                queue.extend(node.children)
        list.sort(key = lambda x: x.index)
        return list

    def keyWords(self):
        '''
        :return: the list of wordNodes who's parent has a non-neutral score
        '''
        return [word for word in self.wordNodes() if word.parent.label != '2']

    def toPTB(self):
        '''
        :return: the PTB format sentence starting from this node
        '''
        if self.children[0].isLeaf() and self.children[1].isLeaf():
            x = '(' + self.label + ' (' + self.children[0].label + ' ' + self.children[0].children[0].word + ') (' + self.children[1].label + ' ' + self.children[1].children[0].word + '))'
        elif self.children[0].isLeaf() and (not self.children[1].isLeaf()):
            x = '(' + self.label + ' (' + self.children[0].label + ' ' + self.children[0].children[0].word + ') ' + self.children[1].toPTB() + ')'
        elif (not self.children[0].isLeaf()) and self.children[1].isLeaf():
            x = '(' + self.label + ' ' + self.children[0].toPTB() + ' (' + self.children[1].label + ' ' + self.children[1].children[0].word + '))'
        else:
            x = '(' + self.label + ' ' + self.children[0].toPTB() + ' ' + self.children[1].toPTB() + ')'
        return x


class ScoreTree(object):
    def __init__(self, sentence):
        self.root = self.__gen(sentence)

    def __gen(self, line):
        '''
        :param line: a PTB sentence with score labels
        :return: the root node of the labelTree
        '''
        root = LabelNode(label =line[1], parent = None, children = [], index = 0)
        current = root
        counter = 1
        for i in range(1, len(line)):
            if line[i] == '(':
                if line[i+3] == '(': #if this is not a word node
                    newNode = LabelNode(label=line[i + 1], parent=current, children=[], index = counter)
                    counter += 1

                else: #if this is a word node
                    newWord = ""
                    j = i+3
                    while(line[j] != ')'):
                        newWord += line[j]
                        j += 1
                    newNode = LabelNode(label=line[i + 1], parent=current, children = [], index = counter)
                    counter += 1
                    newWordNode = WordNode(label = line[i + 1], word=newWord, parent=newNode, index=counter)
                    counter += 1
                    newNode.children.append(newWordNode)
                current.children.append(newNode)
                current = newNode
            elif line[i] == ')':
                current = current.parent
        return root

    def allNodes(self):
        '''
        :return: the list of all nodes in the tree, unsorted, wordNodes not included
        '''
        l = []
        temp = []
        temp.append(self.root)
        while len(temp) != 0:
            x = temp.pop(0)
            l.append(x)
            if not(x.isLeaf()):
                for child in x.children:
                    temp.append(child)
        return l

    def toGraphInput(self):
        '''
        :return: convert the tree to the input format for Graphviz(a visualization app)
        '''
        queue = []
        queue.append(self.root)
        output_str = "digraph G{"
        #print("digraph G{")
        while(len(queue) != 0):
            node = queue.pop(0)
            if type(node) is LabelNode:
                queue += node.children
            #output
            if type(node) is LabelNode:
                output_str += 'Node{0} [label="{1}"]\n'.format(node.index,node.label)
                for child in node.children:
                    output_str += 'Node{0} -> Node{1}\n'.format(node.index,child.index)
            else:
                output_str += 'Node{0} [label="{1}"]\n'.format(node.index,node.word)
        output_str += '}'
        return output_str

    def wordNodes(self):
        '''
        :return: the list of all wordNodes in the tree, sorted by their order in the raw sentence
        '''
        return self.root.wordNodes()

    def keyWords(self):
        '''
        :return: the list of wordNodes who's parent has a non-neutral score
        '''
        return self.root.keyWords()

    def __keyPaths(self):
        '''
        :return: the list of paths from keyWords to root
        '''
        list = []
        for keyWord in self.keyWords():
            current = keyWord
            temp = []
            while not current.isRoot():
                temp.append(current)
                current = current.parent
            temp.append(self.root)
            list.append(temp)
        return list

    def keyNodes(self):
        '''
        :return: a list of key nodes defined by the cross-point algorithm, sorted by their index, wordNodes included
        '''
        list = []
        keyPaths = self.__keyPaths()

        if len(keyPaths) == 0: # type1 tree
            return list
        elif len(keyPaths) == 1: # type2 tree
            path = keyPaths[0]
            del path[2:-1]
            path.reverse()
            return path
        else: # type3 and type4 tree
            list.append(keyPaths[0][-1]) # Add the root node

            for i in range(len(keyPaths)-1):
                current = keyPaths[i][::-1]
                next = keyPaths[i+1][::-1]
                j = 1
                while current[j].index == next[j].index and j < min(len(current), len(next)):
                    j += 1
                if j != 1:
                    list.append(current[j-1])
                list.append(current[-1])
                list.append(current[-2])

            list.append(keyPaths[-1][0]) # Add the wordNode in the last keyPath
            list.append(keyPaths[-1][1]) # Add the leaf node in the last keyPath

            list.sort(key=lambda node: node.index)
            return list

    def __simplifyWithoutTypeChecking(self):
        '''
        :return: the root of the simplified tree.
                    For type1 tree: do nothing, just return the root node of the orignal tree
                    For type2, type3 tree: simplify the subtree containing keyWords, leaving the other part untouched
                    For type4 tree: totally simplified
        '''
        keyNodes = self.keyNodes()
        if keyNodes:
            root = keyNodes[0]
            for node in keyNodes[1:]:
                current = node
                while not (current.parent in keyNodes):
                    current = current.parent
                if current.parent.children[0] == current:
                    current.parent.children[0] = node
                else:
                    current.parent.children[1] = node
            return root
        else:
            return self.root

    def simplify(self):
        keyWords_left = self.root.children[0].keyWords()
        keyWords_right = self.root.children[1].keyWords()

        root = self.__simplifyWithoutTypeChecking()

        if not keyWords_left:
            root.children[0] = LabelNode(label='2', parent=root.children[0], children=[], index=None)
            starter = WordNode(label='2', parent=root.children[0], word="startSentence", index=None)
            root.children[0].children.append(starter)
        if not keyWords_right:
            root.children[1] = LabelNode(label='2', parent=root.children[1], children=[], index=None)
            ender = WordNode(label='2', parent=root.children[0], word="endSentence", index=None)
            root.children[1].children.append(ender)
        return root.toPTB()



    def toPTB(self):
        '''
        :return: convert the tree to PTB format
        '''
        return self.root.toPTB()


    def toS(self):
        '''
        :return: the raw sentence (this method is kind of problematic. Escape Characters?)
        '''
        sentence = ""
        for wordNode in self.wordNodes():
            if re.match(r"^'[a-zA-Z]+", wordNode.word): # Check for 's, 't and 'll
                sentence += wordNode.word
            elif wordNode.word == '``': # Check for ``
                sentence += ' "'
            elif wordNode.word == "''": # Check for ''
                sentence += '"'
            elif re.match(r"^[^a-zA-Z0-9]+$",wordNode.word): # Check whether it is a punctuation
                sentence += wordNode.word
            else:
                if sentence and sentence[-1] == '"':
                    sentence += wordNode.word
                else:
                    sentence += ' ' + wordNode.word
        return sentence[1:].replace('\\', '')

    def treeType(self):
        keyWords_left = self.root.children[0].keyWords()
        keyWords_right = self.root.children[1].keyWords()
        if (not keyWords_left) and (not keyWords_right): # type_1
            return 1
        elif len(keyWords_left + keyWords_right) == 1: #type_2
            return 2
        elif (not keyWords_right) or (not keyWords_left): # type_3
            return 3
        else: # type_4
            return 4

