from maltypes import *

def pr_str(out: MalType, print_readably: bool=False) -> str:
    if type(out) is MalSymbol:
        return out.val
    elif type(out) is MalNumber:
        return out.val
    elif type(out) is MalList:
        return f"({' '.join([pr_str(v) for v in out.val])})"
    elif type(out) is MalVector:
        return f"[{' '.join([pr_str(v) for v in out.val])}]"
    elif type(out) is MalDict:
        return f"{{{', '.join([pr_str(k, print_readably)+' '+pr_str(out.val[k], print_readably) for k in out.val])}}}"
    elif type(out) is MalString:
        if print_readably:
            return '"'+out.val[1:-1].replace('\\','\\\\')\
                                    .replace('\n','\\n')\
                                    .replace('"','\\"')+'"'
        else:
            return out.val
    else:
        return out.val