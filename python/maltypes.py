from typing import Any, List, Dict

class MalType:
    def __init__(self, val=None):
        self.val = val

    def quote(self):
        return str(self.val)

class MalList(MalType):
    def __init__(self, val=None):
        self.val: List[MalType] = []

    def quote(self):
        return f"({' '.join([v.quote() for v in self.val])})"

class MalNumber(MalType):
    def __init__(self, val=None):
        try:
            self.val = val
        except:
            raise Exception("cannot convert string to int", val)

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
    def __init__(self, val=None):
        self.val: List = []

    def quote(self):
        return f"[{', '.join([v.quote() for v in self.val])}]"

class MalDict(MalType):
    def __init__(self, val=None):
        self.val: Dict[MalType, MalType] = {}

    def quote(self):
        return f"{{{', '.join([k.quote()+' '+self.val[k].quote() for k in self.val])}}}"