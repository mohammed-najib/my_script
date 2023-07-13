from tokens import (
    Boolean,
    Comparison,
    Declaration,
    Float,
    Integer,
    Operation,
    Reserved,
    Token,
    Variable,
)


class Lexer:
    digits = "0123456789"
    letters = "abcdefghijklmnopqrstuvwxyz"
    operations = "+-*/()="
    stopwords = [" "]
    # declarations = ["let", "const"]
    declarations = ["make"]
    booleans = ["and", "or", "not"]
    comparisons = ["?=", "!=", "<", ">", "<=", ">="]
    # comparisons = ["is", "is not", "less than", "greater than", "less than or equal to", "greater than or equal to"]
    specialCharecters = "><=!?"
    # reserved = ["let", "const", "and", "or", "not", "is", "is not", "less than", "greater than", "less than or equal to", "greater than or equal to"]
    reserved = ["if", "elif", "else", "do", "while"]

    def __init__(self, text: str) -> None:
        self.text: str = text
        self.idx: int = 0
        self.tokens: list[Token | None] = []
        self.char = self.text[self.idx]
        self.token = None

    def tokenize(self) -> list[Token | None]:
        while self.idx < len(self.text):
            if self.char in Lexer.digits:
                self.token = self.extract_number()
            elif self.char in Lexer.operations:
                self.token = Operation(self.char)
                self.advance()
            elif self.char in Lexer.stopwords:
                self.advance()

                continue
            elif self.char in Lexer.letters:
                word = self.extract_word()
                if word in Lexer.declarations:
                    self.token = Declaration(word)
                elif word in Lexer.booleans:
                    self.token = Boolean(word)
                elif word in Lexer.reserved:
                    self.token = Reserved(word)
                else:
                    self.token = Variable(word)
            elif self.char in Lexer.specialCharecters:
                coparisonOperator = ""
                while self.char in Lexer.specialCharecters and self.idx < len(
                    self.text
                ):
                    coparisonOperator += self.char
                    self.advance()
                self.token = Comparison(coparisonOperator)

            self.tokens.append(self.token)

        return self.tokens

    def extract_number(self) -> Token | None:
        number = ""
        isFloat = False
        while (self.char in Lexer.digits or self.char == ".") and self.idx < len(
            self.text
        ):
            if self.char == ".":
                if isFloat:
                    self.advance()

                    return None

                isFloat = True
            number += self.char
            self.advance()
        return Integer(number) if not isFloat else Float(number)

    def extract_word(self) -> str:
        word = ""
        while self.char in Lexer.letters and self.idx < len(self.text):
            word += self.char
            self.advance()

        return word

    def advance(self) -> None:
        self.idx += 1
        if self.idx < len(self.text):
            self.char = self.text[self.idx]
