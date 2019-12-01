#!/usr/bin/env python3

def READ(in_var):
    return in_var

def EVAL(in_var):
    return in_var

def PRINT(in_var):
    return in_var

def rep(in_var):
    readResult = READ(in_var)
    evalResult = EVAL(readResult)
    printResult = PRINT(evalResult)
    return printResult

def main():
    while True:
        # TODO history + editing of history
        try:
            in_str = input("user> ")
            print(rep(in_str))
        except EOFError:
            print("\nexit")
            break

if __name__ == '__main__':
    main()
