from interpreter import Interpreter
from lexer import Lexer
from parserr import Parser
from data import Data

base = Data()

while True:
    text = input("MyScript: ")

    tokenizer = Lexer(text)
    tokens = tokenizer.tokenize()

    print(tokens)

    parser = Parser(tokens)
    tree = parser.parse()

    print(tree)

    interpreter = Interpreter(tree, base)
    result = interpreter.interpret()

    if result is not None:
        print(result)
