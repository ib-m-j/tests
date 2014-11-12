from pypeg2 import *


inp = 'loop(tag, start, action)'
basic = '(tag, start, axxction)'

class TagType(Keyword):
    grammar = Enum( K('end'), K('start'))

class Action(str):
    grammar = word

class BasicObject(str):
    grammar = name(),',',attr('tagtype', TagType),',',attr('action', Action)

class Loop(str):
    grammar = 'loop','(', attr('basic', BasicObject),')'


if __name__ == "__main__":
    r = parse(inp, Loop)
    print(r.basic.name, 'ccc', r.basic.action, 'end')
