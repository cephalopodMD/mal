from maltypes import *
from reader import *
from printer import *

def eq(a, b):
    if type(a) in [MalList, MalVector] and type(b) in [MalList, MalVector]:
        return len(a.val) == len(b.val) and [0 for aa,bb in zip(a.val, b.val)
            if not ns['='](aa, bb).val] == []
    else:
        return type(a) == type(b) and a.val == b.val
def slurp(s):
    with open(s,"r") as f:
        return '\n'.join(f.readlines())

def nth(l, n):
    if n.val >= len(l.val):
        raise MalException('invalid list index')
    return l.val[n.val]

ns = {
    'exit': lambda: exit(),
    '+': lambda a,b: a.add(b),
    '-': lambda a,b: a.sub(b),
    '*': lambda a,b: a.mul(b),
    '/': lambda a,b: a.div(b),
    '=': lambda a,b: MalBool(eq(a,b)),
    '<': lambda a,b: MalBool(a.val < b.val),
    '>': lambda a,b: MalBool(a.val > b.val),
    '<=': lambda a,b: MalBool(a.val <= b.val),
    '>=': lambda a,b: MalBool(a.val >= b.val),
    'list': lambda *l: MalList(l),
    'list?': lambda l: MalBool(type(l) is MalList),
    'empty?': lambda l: MalBool(l.val == []),
    'count': lambda l, *largs: MalNumber(len(l.val) if type(l) in [MalList, MalVector] else 0),
    'pr-str': lambda *s: MalString(' '.join([pr_str(v, True) for v in s])),
    'str': lambda *s: MalString(''.join([pr_str(v, False) for v in s])),
    'prn': lambda *s: MalNil(print(' '.join([pr_str(v, True) for v in s]))),
    'println': lambda *s: MalNil(print(' '.join([pr_str(v, False) for v in s]))),
    'read-string': lambda s: read_str(s.val),
    'slurp': lambda s: MalString(slurp(s.val)),
    'atom': lambda a: MalAtom(a),
    'atom?': lambda a: MalBool(type(a) is MalAtom),
    'deref': lambda a: a.val,
    'reset!': lambda a, v: a.reset(v),
    'cons': lambda a, l: MalList([a] + list(l.val)),
    'concat': lambda *l: MalList([item for sublist in l for item in list(sublist.val)]),
    'nth': nth,
    'first': lambda l: l.val[0] if type(l) is not MalNil and len(l.val) else MalNil(),
    'rest': lambda l: MalList(l.val[1:]) if type(l) is not MalNil and len(l.val) else MalList(),
}