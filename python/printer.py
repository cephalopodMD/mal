from maltypes import *

def pr_str(out: MalType, print_readably: bool=False) -> str:
    if type(out) is MalSymbol:
        return out.val
    elif type(out) is MalNumber:
        return str(out.val)
    elif type(out) is MalList:
        return f"({' '.join([pr_str(v, print_readably) for v in out.val])})"
    elif type(out) is MalVector:
        return f"[{' '.join([pr_str(v, print_readably) for v in out.val])}]"
    elif type(out) is MalDict:
        keys = [k if k[0] == ':' else '"'+k+'"' for k in out.val]
        values = [pr_str(v, print_readably) for v in out.val.values()]
        return '{'+', '.join([f"{k} {v}" for k, v in zip(keys, values)])+'}'
    elif type(out) is MalString:
        if print_readably:
            return '"'+out.val.replace('\\','\\\\')\
                              .replace('\n','\\n')\
                              .replace('"','\\"')+'"'
        else:
            return out.val
    elif type(out) is MalFn or type(out) is MalCustomFn:
        return '#<function>'
    elif type(out) is MalNil:
        return 'nil'
    elif isinstance(out, MalBool):
        return str(out.val).lower()
    elif type(out) is MalAtom:
        return f'(atom {pr_str(out.val, print_readably)})'
    else:
        return out.val