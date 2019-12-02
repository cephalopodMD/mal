#!/usr/bin/env python3.8
from reader import read_str
from printer import pr_str
from maltypes import *
from typing import Dict, Callable

def READ(in_text) -> MalType:
    try:
        return read_str(in_text)
    except EOFError:
        print("\nexit")
        exit()

def eval_ast(ast: MalType, env: Dict[str, Any]):
    if type(ast) is MalSymbol and not ast.val[0] == ':':
        if ast.val not in env:
            raise MalException(f'symbol {ast.val} not found')
        return env.get(ast.val)
    elif type(ast) is MalList:
        return MalList([EVAL(a, env) for a in ast.val])
    elif type(ast) is MalVector:
        return MalVector([EVAL(a, env) for a in ast.val])
    elif type(ast) is MalDict:
        return MalDict({EVAL(a, env): EVAL(ast.val[a], env) for a in ast.val})
    else:
        return ast

def EVAL(ast: MalType, env: Dict[str, Any]) -> MalType:
    if type(ast) is MalList:
        if len(ast.val) == 0:
            return ast
        else:
            eval_list = eval_ast(ast, env)
            return apply(eval_list.val[0], eval_list.val[1:])
    else:
        return eval_ast(ast, env)

def apply(fn: Callable, args: List[MalType]):
    return fn(*args)

def PRINT(result):
    return pr_str(result, True)

repl_env = {'+': lambda a,b: a.add(b),
            '-': lambda a,b: a.sub(b),
            '*': lambda a,b: a.mul(b),
            '/': lambda a,b: a.div(b)}
def rep(in_text):
    try:
        ast = READ(in_text)
        result = EVAL(ast, repl_env)
        out_text = PRINT(result)
        return out_text
    except MalException as e:
        return str(e)
    except Exception as e:
        raise e

def main():
    while True:
        # TODO history + editing of history
        in_var = input("user> ")
        if in_var:
            print(rep(in_var))

if __name__ == '__main__':
    main()
