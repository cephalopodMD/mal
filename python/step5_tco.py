#!/usr/bin/env python3.8
from reader import read_str
from printer import pr_str
from maltypes import *
from typing import Dict, Callable, cast
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
        return env.get(cast(MalSymbol, ast))
    elif type(ast) is MalList:
        return MalList([EVAL(a, env) for a in ast.val])
    elif type(ast) is MalVector:
        return MalVector([EVAL(a, env) for a in ast.val])
    elif type(ast) is MalDict:
        return MalDict({EVAL(a, env): EVAL(ast.val[a], env) for a in ast.val})
    else:
        return ast

def EVAL(ast: MalType, env: Env) -> MalType:
    while True:
        if type(ast) is MalList:
            if len(ast.val) == 0:
                return ast
            else:
                # apply
                if type(special_form := ast.val[0]) is MalSymbol:
                    if special_form.val == 'def!':
                        val = EVAL(ast.val[2], env)
                        env.set(ast.val[1], val)
                        return val
                    elif special_form.val == 'let*':
                        let = ast.val[1].val
                        if len(let)%2 == 1:
                            raise MalException('invalid let')
                        new_env = Env(env)
                        for i in range(0, len(let), 2):
                            new_env.set(let[i], EVAL(let[i+1], new_env))
                        env = new_env
                        ast = ast.val[2]
                        continue
                    elif special_form.val == 'do':
                        if len(ast.val) > 2:
                            eval_ast(MalList(ast.val[1:-1]), env).val[-1]
                        ast = ast.val[-1]
                        continue
                    elif special_form.val == 'if':
                        result = EVAL(ast.val[1], env)
                        if result.val or not (isinstance(result, MalBool) or type(result) == MalNil):
                            ast = ast.val[2]
                            continue
                        elif len(ast.val) == 4:
                            ast = ast.val[3]
                            continue
                        else:
                            return MalNil()
                    elif special_form.val == 'fn*':
                        return MalCustomFn(ast.val[1], ast.val[2], env)
                f, *args = eval_ast(ast, env).val
                if type(f) is MalCustomFn:
                    ast = f.ast
                    env = Env(f.env, f.params.val, args)
                    continue
                else:
                    return f.call(args)
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

def main():

    def eq(a, b):
        if type(a) in [MalList, MalVector] and type(b) in [MalList, MalVector]:
            return len(a.val) == len(b.val) and [0 for aa,bb in zip(a.val, b.val)
                if not ns['='](aa, bb).val] == []
        else:
            return type(a) == type(b) and a.val == b.val
    ns = {
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
    }
    for sym in ns:
        repl_env.set(MalSymbol(sym), MalFn(ns[sym]))

    rep("(def! not (fn* (a) (if a false true)))")

    while True:
        # TODO history + editing of history
        in_var = input("user> ")
        if in_var:
            print(rep(in_var))

if __name__ == '__main__':
    main()
