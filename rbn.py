from re import search, match, findall
from math import sin, cos, tan, pow, log, pi
from pprint import pprint
import dill as pickle

# def get_infix_notation(string: str) -> list
# def build(tokens: list) -> list
# def calculate(tokens: list, var: float=0.0) -> float

with open('./opdata', 'rb') as file:
    op = pickle.load(file) # load operator dictionary


def get_infix_notation(string: str) -> list:
    tokens = findall(r'^-\d+|(?<=\()-\d+|\d+\.\d+|\w+|[.\S]', string) # split into token
    return tokens

def build(tokens: list) -> list:
    # shunting-yard algorithm
    result = []
    stack = [] # operator stack

    for token in tokens:
        if(search('\d+', token)): # if digit
            result.append(token)
        if(token in op): # if operator
            try:
                while(stack[-1] != '(' and
                     op[token]['precedence'] > op[stack[-1]]['precedence'] or
                     (op[token]['precedence'] == op[stack[-1]]['precedence'] and
                      op[stack[-1]]['associativity'] == 'left')):
                    result.append(stack.pop())
            except IndexError: # ignore when operator stack is empty
                pass
            except KeyError: # ignore when token is '(' or ')'
                pass
            stack.append(token)
        if(search('\(', token)): # if open bracket
            stack.append(token)
        if(search('\)', token)): # if close bracket
            while(stack[-1] != '('): # while there is open bracket
                result.append(stack.pop()) # pop every operator in stack
            stack.pop() # remove ')' pair

    while(len(stack) != 0): # while stack is empty
        result.append(stack.pop()) # pop all operator into result

    return result

def calculate(tokens: list, var: float=0.0) -> float:
    # Reverse Polish notation algorithm
    stack = [] # stack to store operand

    for token in tokens: #for each token in the postfix expression:
        if token in op:  #if token is an operator:
            if op[token]['type'] == 'binary':
                operand2 = float(stack.pop()) #operand_2 ← pop from the stack
                operand1 = float(stack.pop()) #operand_1 ← pop from the stack
                #result ← evaluate token with operand_1 and operand_2
                result = op[token]['func'](operand1, operand2)
            elif op[token]['type'] == 'unary':
                #else if token is an operand:
                operand = float(stack.pop())
                result = op[token]['func'](operand)
            elif op[token]['type'] == 'constant':
                result = op[token]['func']()
            elif op[token]['type'] == 'variable':
                result = op[token]['func'](var)
            stack.append(result) # push result back onto the stack
        else:
            stack.append(token) # push operand into stack
    return stack[0] #result ← pop from the stack


if __name__ == '__main__':
    string = '1/100*10'
    print(string)
    var = 0
    infix_tokens = get_infix_notation(string)
    print(infix_tokens)
    rpn_tokens = build(infix_tokens)
    print(rpn_tokens)
    for x in range(0, 1000):
        print(string, '| x='+str(x))
        print(calculate(rpn_tokens, x))
