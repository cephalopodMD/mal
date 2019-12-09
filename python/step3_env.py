#!/usr/bin/env python3.8
from reader import read_str
from printer import pr_str
from maltypes import *
from typing import Dict, Callable
from env import Env

repl_env = Env()

def READ(in_text) -> MalType:
    try:
        return read_str(in_text)
    except EOFError:
        print("\nexit")
        exit()

def eval_ast(ast: MalType, env: Env):
    if type(ast) is MalSymbol and not ast.val[0] == ':':
        return env.get(ast)
    elif type(ast) is MalList:
        return MalList([EVAL(a, env) for a in ast.val])
    elif type(ast) is MalVector:
        return MalVector([EVAL(a, env) for a in ast.val])
    elif type(ast) is MalDict:
        return MalDict({EVAL(a, env): EVAL(ast.val[a], env) for a in ast.val})
    else:
        return ast

def EVAL(ast: MalType, env: Env) -> MalType:
    if type(ast) is MalList:
        if len(ast.val) == 0:
            return ast
        else:
            # apply
            if type(ast.val[0]) is MalSymbol:
                if ast.val[0].val == 'def!':
                    val = EVAL(ast.val[2], env)
                    env.set(ast.val[1], val)
                    return val
                elif ast.val[0].val == 'let*':
                    let = ast.val[1].val
                    if len(let)%2 == 1:
                        raise MalException('invalid let')
                    new_env = Env(env)
                    for i in range(0, len(let), 2):
                        new_env.set(let[i], EVAL(let[i+1], new_env))
                    return EVAL(ast.val[2], new_env)
            eval_list = eval_ast(ast, env)
            return eval_list.val[0]( *(eval_list.val[1:]) )
    else:
        return eval_ast(ast, env)

def PRINT(result):
    return pr_str(result, True)

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
    repl_env.set(MalSymbol('+'), lambda a,b: a.add(b))
    repl_env.set(MalSymbol('-'), lambda a,b: a.sub(b))
    repl_env.set(MalSymbol('*'), lambda a,b: a.mul(b))
    repl_env.set(MalSymbol('/'), lambda a,b: a.div(b))
    while True:
        # TODO history + editing of history
        in_var = input("user> ")
        if in_var:
            print(rep(in_var))

if __name__ == '__main__':
    main()
