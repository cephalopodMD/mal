#!/usr/bin/env python3.8
from reader import read_str
from printer import pr_str
from maltypes import MalType

def READ(in_text) -> MalType:
    try:
        return read_str(in_text)
    except EOFError:
        print("\nexit")
        exit()

def EVAL(ast: MalType) -> MalType:
    return ast

def PRINT(result):
    return pr_str(result, True)

def rep(in_text):
    try:
        ast = READ(in_text)
        result = EVAL(ast)
        out_text = PRINT(result)
        return out_text
    except Exception as e:
        return str(e)

def main():
    while True:
        # TODO history + editing of history
        in_var = input("user> ")
        if in_var:
            print(rep(in_var))

if __name__ == '__main__':
    main()
