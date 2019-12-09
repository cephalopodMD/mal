from typing import Any, Optional
from maltypes import *

class Env:
    def __init__(self, outer=None, binds=None, exprs=[]):
        self.outer: Optional[Env] = outer
        self.data: Any = {}
        if binds:
            for i, b in enumerate(binds):
                if b.val == '&':
                    self.set(binds[i+1], MalList(exprs[i:]))
                    break
                self.set(b, exprs[i])

    def find(self, key: MalSymbol):
        if key.val in self.data:
            return self.data
        elif self.outer:
            return self.outer.find(key)
        else:
            return None

    def get(self, key: MalSymbol):
        if e := self.find(key):
            return e[key.val]
        raise MalException(f'symbol {key.val} not found')

    def set(self, key: MalSymbol, value: MalType):
        self.data[key.val] = value