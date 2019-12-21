#!/usr/bin/env python3.8
from reader import read_str
from printer import pr_str
from maltypes import *
from typing import Dict, Callable, cast
from env import Env
from core import ns
import sys

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

def is_pair(l: MalType):
    return type(l) in [MalList, MalVector] and l.val != []

def quasiquote(ast: MalType):
    if not is_pair(ast):
        return MalList([MalSymbol('quote'), ast])
    else:
        if ast.val[0].val == 'unquote':
            return ast.val[1]
        if is_pair(ast.val[0]) and ast.val[0].val[0].val == 'splice-unquote':
            return MalList([MalSymbol('concat'), ast.val[0].val[1], quasiquote(MalList(ast.val[1:]))])
    return MalList([MalSymbol('cons'), quasiquote(ast.val[0]), quasiquote(MalList(ast.val[1:]))])

def is_macro_call(ast: MalType, env: Env):
    return type(ast) is MalList and\
        type(arg1 := ast.val[0]) is MalSymbol and\
        env.find(arg1) and\
        isinstance(env.get(arg1), MalFn) and\
        env.get(arg1).is_macro

def macroexpand(ast: MalType, env: Env):
    new_env = env
    while is_macro_call(ast, env):
        macro = env.get(ast.val[0])
        f, *args = eval_ast(ast, env).val
        new_ast = macro.ast
        new_env = Env(macro.env, macro.params.val, args)
        ast = EVAL(new_ast, new_env)
    return ast

def EVAL(ast: MalType, env: Env) -> MalType:
    while True:
        if type(ast) is not MalList:
            return eval_ast(ast, env)
        if len(ast.val) == 0:
            return ast
        if is_macro_call(ast, env):
            ast = macroexpand(ast, env)
            continue
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
            elif special_form.val == 'eval':
                ast = EVAL(ast.val[1], env)
                env = repl_env
                continue
            elif special_form.val == 'swap!':
                atom = eval_ast(ast.val[1], env)
                new_ast = MalList([ast.val[2], atom.val] + ast.val[3:])
                atom.reset(EVAL(new_ast, env))
                return atom.val
            elif special_form.val == 'quote':
                return ast.val[1]
            elif special_form.val == 'quasiquote':
                ast = quasiquote(ast.val[1])
                continue
            elif special_form.val == 'defmacro!':
                val = cast(MalFn, EVAL(ast.val[2], env))
                val.is_macro = True
                env.set(ast.val[1], val)
                return val
            elif special_form.val == 'macroexpand':
                return macroexpand(ast.val[1], env)
        f, *args = eval_ast(ast, env).val
        if type(f) is MalCustomFn:
            ast = f.ast
            env = Env(f.env, f.params.val, args)
            continue
        else:
            return f.call(args)

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
    for sym in ns:
        repl_env.set(MalSymbol(sym), MalFn(ns[sym]))

    #define some funcitons in mal
    rep("(def! not (fn* (a) (if a false true)))")
    rep("(def! load-file (fn* (f) (eval (read-string (str \"(do \" (slurp f) \"\nnil)\")))))")
    rep("(defmacro! cond (fn* (& xs) (if (> (count xs) 0) (list 'if (first xs) (if (> (count xs) 1) (nth xs 1) (throw \"odd number of forms to cond\")) (cons 'cond (rest (rest xs)))))))")

    if len(sys.argv) > 1:
        f = sys.argv[1]
        argv = sys.argv[2:]
        print(sys.argv, f, argv)
        repl_env.set(MalSymbol('*ARGV*'), MalList([MalString(arg) for arg in argv]))
        rep(f'(load-file "{f}")')
        exit()
    else:
        repl_env.set(MalSymbol('*ARGV*'), MalList())

    while True:
        # TODO history + editing of history
        in_var = input("user> ")
        if in_var:
            print(rep(in_var))


if __name__ == '__main__':
    main()
