from pypeg2 import *
import re

class State:
    def __init__(self, parent, type):
        self.states = []
        self.endactions = []
        self.parent = parent
        self.input = ''
        self.level = 0
        self.type = type

    def setInput(self, input):
        self.input = input

    def setStates(self, level):
        self.level = level
        #print(self.input)
        while len(self.input) > 0:
            res = parse(self.input, First1)
            #print('\n',inp)
            print(res)
            print(res.__dict__)
            if 'token' in res.__dict__.keys():
                print('processing', res.token, level)
                child = State(self, res.token)
                child.setInput(res.rest)
                child.setStates(level + 1)
                self.states.append(child)
            elif 'basic' in res.__dict__.keys():
                self.states.append((res.basic.name,res.basic.tagtype,
                                    res.basic.action, res.basic.parameter))
                self.input = res.rest
            elif 'endaction' in res.__dict__.keys():
                self.endactions.append((res.endaction.name,
                                        res.endaction.tagtype))
                self.input = res.rest
            else:
                print("ending")
                if level> 0:
                    print("setting parent", res.rest)
                    self.parent.setInput(res.rest)
                break

            print ("redo",self.level,  self.input)

    def __str__(self):
        res = '{} {} length {}\n'.format(self.level, self.type, len(self.states))
        for s in self.states:
            if isinstance(s, State):
                res = res + '{}child {}\n'.format(self.level*'  ',s.__str__())
            else:
                res = res + '{}{}\n'.format(self.level*'  ',s)
        
        return res

    def go(self):
        for s in self.states:
            if isinstance (s, State):
                print(s)
    

class TagType(Keyword):
    grammar = Enum( K('end'), K('start'))

class Action(Keyword):
    grammar = Enum( K('skip'), K('inc'), K('finish'), K('skip'))

class BasicObject(str):
    grammar = '(', name(),',',attr('tagtype', TagType),',',\
              (attr('action', Action),attr('parameter',optional('(',word),')')),')'

class EndAction(str):
    grammar = '(', name(), ',', attr('tagtype', TagType),')'

class Token(Keyword):
    grammar = Enum( K('loop'))

class First1(str):
    grammar = [(attr('token', Token), '('), (attr('endaction', EndAction)), \
               (attr('basic',BasicObject)),')'] , attr('rest',restline)

def testParse():
    inp = 'loop((endtag, end)(tag, start, finish)loop((tag1, end, skip(a)))) (tag2, start, finish)(tag3, end, inc)'
    parseline = inp
    while len(inp) > 0:
        res = parse(inp, First1)
        #print(res.__dict__)
        print('\n',inp)
        if 'token' in res.__dict__.keys():
            print (res.token)
        elif 'basic' in res.__dict__.keys():
            print (res.basic.name,res.basic.tagtype,res.basic.action)
        elif 'endaction' in res.__dict__.keys():
            print (res.endaction.name,res.endaction.tagtype)
        else:
            print("endbracket")

        inp = res.rest


if __name__ == "__main__":
    #testParse()
    inp = 'loop((endtag, end)(tag, start, finish)loop((tag1, end, skip(a))))(tag2, start, finish)(tag3, end, inc)'
    #inp = 'loop((tag, start, finish)(tag1, end, finish))(tag2, start, finish)(tag3, end, inc))'
    
    top = State(None,'top')
    top.setInput(inp)
    top.setStates(0)

    print(inp)
    print()
    print(top)
