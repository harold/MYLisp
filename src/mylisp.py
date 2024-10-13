import edn_format

def truthy(v): return v not in {None, False, ()}

# mylisp.core
def ml_print(_env, args):
    while args:
        print(args[0], end = " " if len(args) > 1 else "")
        args = args[1:]

def ml_add(env, args):
    return args[0] + args[1]

def ml_equals(env, args):
    return args[0] == args[1]

def ml_and(env, args):
    return truthy(args[0]) and truthy(args[1])

def ml_first(env, args):
    return args[0][0]

def ml_rest(env, args):
    return args[0][1:]

def ml_cons(env, args):
    # the parens and commas on the following line are, um, not optional
    # python is Brain Damage
    return (args[0],) + (args[1:]+((),))[0]

def ml_dir(env, args):
    return tuple(env.keys())

# eval
def eval_items(env, value):
    evaled = ()
    while value:
        evaled = evaled + (eval_value(env, value[0]),)
        value = value[1:]
    return evaled

SYM_DEF = edn_format.loads("def")
SYM_QUOTE = edn_format.loads("quote")
SYM_IF = edn_format.loads("if")

def eval_function_call(env, value):
    verb = value[0]
    if verb == SYM_DEF:
        name = value[1]
        value = value[2]
        env[name] = eval_value(env, value)
        result = name
    elif verb == SYM_QUOTE:
        result = value[1]
    elif verb == SYM_IF:
        condition = value[1]
        true_expr = value[2]
        false_expr = value[3] if len(value) > 2 else None
        if(truthy(eval_value(env, condition))):
            result = eval_value(env, true_expr)
        else:
            result = eval_value(env, false_expr)
    else:
        evaled_list = eval_items(env, value)
        f = evaled_list[0]
        args = evaled_list[1:]
        result = f(env, args)
    return result

def eval_value(env, value):
    if None == value: return ()
    if isinstance(value, edn_format.edn_lex.Symbol):
        return env[value]
    if isinstance(value, tuple):
        return eval_function_call(env, value)
    return value

def repl(env):
    while True:
        value = edn_format.loads(input("mylisp> "))
        result = eval_value(env, value)
        print(edn_format.dumps(result))

if __name__ == "__main__":
    environment = {}
    environment[edn_format.loads("language")] = "MyLisp"
    environment[edn_format.loads("version")] = "0.1"
    environment[edn_format.loads("print")] = ml_print
    environment[edn_format.loads("+")] = ml_add
    environment[edn_format.loads("=")] = ml_equals
    environment[edn_format.loads("and")] = ml_and
    environment[edn_format.loads("first")] = ml_first
    environment[edn_format.loads("rest")] = ml_rest
    environment[edn_format.loads("cons")] = ml_cons
    environment[edn_format.loads("dir")] = ml_dir
    repl(environment)
