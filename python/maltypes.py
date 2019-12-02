from typing import Any, List, Dict

class MalException(Exception): pass

class MalType:
    def __init__(self, val=None):
        self.val = val

    def quote(self):
        return str(self.val)

class MalList(MalType):
    def __init__(self, val: List[MalType]=None):
        self.val: List[MalType] = val or []

    def quote(self):
        return f"({' '.join([v.quote() for v in self.val])})"

class MalNumber(MalType):
    def __init__(self, val=None):
        try:
            self.val = int(val)
        except:
            raise MalException("cannot convert string to int", val)

    def add(self, n):
        return MalNumber(self.val+n.val)

    def sub(self, n):
        return MalNumber(self.val-n.val)

    def mul(self, n):
        return MalNumber(self.val*n.val)

    def div(self, n):
        return MalNumber(self.val/n.val)

class MalSymbol(MalType):
    def __init__(self, val=None):
        self.val: str = val

class MalNil(MalType):
    def __init__(self, val=None):
        self.val: None = None

    def quote(self):
        return "Nil"

class MalTrue(MalType):
    def __init__(self, val=None):
        self.val: bool = True

class MalFalse(MalType):
    def __init__(self, val=None):
        self.val: bool = False 

class MalString(MalType):
    def __init__(self, val=None):
        self.val:str = val

class MalVector(MalType):
    def __init__(self, val: List[MalType]=None):
        self.val: List[MalType] = val or []

    def quote(self):
        return f"[{', '.join([v.quote() for v in self.val])}]"

class MalDict(MalType):
    def __init__(self, val=None):
        self.val: Dict[str, MalType] = val or {}

    def quote(self):
        return f"{{{', '.join([k.quote()+' '+self.val[k].quote() for k in self.val])}}}"