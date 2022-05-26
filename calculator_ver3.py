#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_times(line, index):
    token = {'type': 'TIMES'}
    return token, index + 1

def read_divided(line, index):
    token = {'type': 'DIVIDED'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    brc = []
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
            tokens.append(token)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
            tokens.append(token)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
            tokens.append(token)
        elif line[index] == '*':
            (token, index) = read_times(line, index)
            tokens.append(token)
        elif line[index] == '/':
            (token, index) = read_divided(line, index)
            tokens.append(token)
        elif line[index] == '(':
            brc.append(len(tokens))
            index += 1
        elif line[index] == ')':
            start = brc[-1]
            end = len(tokens)
            del brc[-1]
            tmp = evaluate(tokens[start:end])
            del tokens[start:end]
            tokens.insert(start,{'type':'NUMBER', 'number': tmp})
            index += 1
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
    return tokens

def evaluate(tokens):
    print(tokens)
    new_tokens = first_evaluate(tokens)
    print(new_tokens)
    answer = second_evaluate(new_tokens)
    return answer

def first_evaluate(tokens):
    if tokens[0]['type'] == 'MINUS':
        tokens.insert(0,{'type':'NUMBER', 'number':0})
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'TIMES':
                if tokens[index - 2]['type'] == 'NUMBER':
                    answer = tokens[index - 2]['number'] * tokens[index]['number']
                    token = {'type': 'NUMBER', 'number': answer}
                    del tokens[index-2:index+1]
                    tokens.insert(index - 2, token)
                    index -= 2
            elif tokens[index - 1]['type'] == 'DIVIDED':
                if tokens[index - 2]['type'] == 'NUMBER':
                    answer = tokens[index - 2]['number'] / tokens[index]['number']
                    token = {'type': 'NUMBER', 'number': answer}
                    del tokens[index-2:index+1]
                    tokens.insert(index - 2, token)  
                    index -= 2
        index += 1
    return tokens

def second_evaluate(tokens):
    answer = 0
    if tokens[0]['type'] == 'NUMBER':
        tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("2+3*5")
    test("6/2*3.5")
    test("5+5-6*2")
    test("1.2+3.2*2-1")
    test("33-2.3-12*2.2")
    test("3.2*(3/(1+1))")
    test("6+(25-3)*(4-10)")
    test("13+(2-(-4))*(-1.5)")
    test("(5-(-2))*8")
    test("-6-12/(-3)")
    test("12*(3-1.2)/(2+3)")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)