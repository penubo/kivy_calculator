from math import sin, cos, pow, tan, log, pi
from pprint import pprint
import dill as pickle

associativity = {
    'x' : 'right',
    'π' : 'right',
    'sin' : 'right',
    'cos' : 'right',
    'tan' : 'right',
    'log' : 'right',
    '!' : 'left',
    '^' : 'right',
    '*' : 'left',
    '/' : 'left',
    '+' : 'left',
    '-' : 'left'
}

precedence = {
    'x' : 1,
    'π' : 1,
    'sin' : 2,
    'cos' : 2,
    'tan' : 2,
    'log' : 2,
    '!' : 2,
    '^' : 3,
    '*' : 3,
    '/' : 3,
    '+' : 4,
    '-' : 4
}

op_type = {
    'x' : 'variable',
    'π' : 'constant',
    'sin' : 'unary',
    'cos' : 'unary',
    'tan' : 'unary',
    'log' : 'unary',
    '!' : 'unary',
    '^' : 'binary',
    '*' : 'binary',
    '/' : 'binary',
    '+' : 'binary',
    '-' : 'binary'
}

operators = {
    'x' : lambda x: x,
    'π' : lambda : pi,
    'sin' : lambda x: sin(x),
    'cos' : lambda x: cos(x),
    'tan' : lambda x : tan(x),
    'log' : lambda x : log(x),
    '!' : (lambda f: (lambda x: f(lambda v: x(x)(v)))(lambda x: f(lambda v: x(x)(v))))(lambda f: (lambda i: 1 if (i == 0) else i * f(i - 1))),
    '^' : lambda x, y: pow(x, y),
    '*' : lambda x, y: x * y,
    '/' : lambda x, y: x / y,
    '+' : lambda x, y: x + y,
    '-' : lambda x, y: x - y
}


if __name__ == '__main__':
    data = {}
    for token in operators:
        data[token] = {
            'func' : operators[token],
            'associativity' : associativity[token],
            'precedence' : precedence[token],
            'type' : op_type[token]
        }
    with open('opdata', 'wb') as file:
        pickle.dump(data, file)
    with open('opdata', 'rb') as file:
        pprint(pickle.load(file))
