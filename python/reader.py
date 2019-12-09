import re
from typing import List, Any
from maltypes import *
from printer import pr_str

class Reader:
    def __init__(self, tokens: List[str]):
        self.tokens: List[str] = tokens
        self.position: int = 0
        self.balance: List[str] = []

    def next(self) -> str:
        result = self.peek()
        self.position += 1
        return result

    def peek(self) -> str:
        return self.tokens[self.position]

    def read_form(self) -> MalType:
        if(self.peek()[0] == '('):
            return self.read_list()
        elif(self.peek()[0] == '['):
            return self.read_vector()
        elif(self.peek()[0] == '{'):
            return self.read_dict()
        else:
            return self.read_atom()

    def read_list(self) -> MalList:
        self.next()
        result = MalList()
        while self.peek() != ')':
            if self.position == len(self.tokens) - 1:
                raise MalException('.*(EOF|end of input|unbalanced).*')
            result.val.append(self.read_form())
        self.next()
        return result

    def read_vector(self) -> MalVector:
        self.next()
        result = MalVector()
        while self.peek() != ']':
            if self.position == len(self.tokens) - 1:
                raise MalException('.*(EOF|end of input|unbalanced).*')
            result.val.append(self.read_form())
        self.next()
        return result

    def read_dict(self) -> MalDict:
        self.next()
        result = MalDict()
        while self.peek() != '}':
            if self.position == len(self.tokens) - 1:
                raise MalException('.*(EOF|end of input|unbalanced).*')
            key = pr_str(self.read_form())
            if self.peek() == '}' or self.position == len(self.tokens) - 1:
                raise MalException('.*(EOF|end of input|unbalanced).*')
            result.val[key] = self.read_form()
        self.next()
        return result

    def read_atom(self) -> MalType:
        token = self.next()
        if re.match(r"-?\d+", token):
            return MalNumber(token)
        elif token == "true":
            return MalTrue()
        elif token == "false":
            return MalFalse()
        elif token == "nil":
            return MalNil()
        elif token == "'":
            return MalType(f"(quote {self.read_form().quote()})")
        elif token == "`":
            return MalType(f"(quasiquote {self.read_form().quote()})")
        elif token == "~":
            return MalType(f"(unquote {self.read_form().quote()})")
        elif token == "~@":
            return MalType(f"(splice-unquote {self.read_form().quote()})")
        elif token == "@":
            return MalType(f"(deref {self.read_form().quote()})")
        elif token == ";":
            self.position == len(self.tokens) - 1
            return MalType()
        elif token[0] == '"':
            if token == '"' or (not token[-1] == '"') or token.replace('\\\\','')[-2] == '\\':
                raise MalException('.*(EOF|end of input|unbalanced).*')
            string_token = ''
            special = False
            tok = token[1:-1]
            for a, b in zip(tok[:-1], tok[1:]):
                if special:
                    special = False
                    continue
                elif a == '\\':
                    if b == '\\':
                        string_token += '\\'
                        special = True
                    elif b == 'n':
                        string_token += '\n'
                        special = True
                    elif b == '"':
                        string_token += '"'
                        special = True
                else:
                    string_token += a
            if not special and tok:
                string_token += tok[-1]
            #string_token = token[1:-1].replace('\\"','"')\
            #                          .replace('\\n','\n')\
            #                          .replace('\\\\','\\')
            return MalString(string_token)

        return MalSymbol(token)

def read_str(input_string: str) -> MalType:
    tokens = tokenize(input_string)
    reader = Reader(tokens)
    return reader.read_form()

def tokenize(input_string: str) -> List[str]:
    return re.findall(r"[\s,]*(~@|[\[\]{}()'`~^@]|\"(?:\\.|[^\\\"])*\"?|;.*|[^\s\[\]{}('\"`,;)]*)", input_string)
