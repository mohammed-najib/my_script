from constants import (
    BOOLEAN,
    COMPARISON,
    DECLARATION,
    DIVIDE,
    DO,
    ELIF,
    ELSE,
    FLOAT,
    IF,
    INTEGER,
    MINUS,
    MULTIPLY,
    NOT,
    OPERATION,
    PLUS,
    VARIABLE,
    WHILE,
)
from lexer import Token


class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.idx = 0
        self.token = self.tokens[self.idx]

    def factor(self) -> list | Token | None:
        if self.token != None:
            if self.token.type == INTEGER or self.token.type == FLOAT:
                return self.token

            elif self.token.value == "(":
                self.advance()
                expression = self.boolean_expression()

                return expression
            elif self.token.value == NOT:
                operator = self.token
                self.advance()

                return [operator, self.boolean_expression()]
            elif self.token.type.startswith(VARIABLE):
                return self.token
            elif self.token.value == PLUS or self.token.value == MINUS:
                operator = self.token
                self.advance()
                operand = self.factor()

                if isinstance(operand, Token):
                    return [operator, operand]

    def term(self) -> list[Token] | Token | None:
        left_node = self.factor()
        self.advance()

        while self.token != None and (
            self.token.value == MULTIPLY or self.token.value == DIVIDE
        ):
            operation = self.token
            self.advance()
            right_node = self.factor()
            self.advance()
            left_node = [left_node, operation, right_node]

        return left_node

    def expression(self) -> list[Token] | Token | None:
        left_node = self.term()

        while self.token != None and (
            self.token.value == PLUS or self.token.value == MINUS
        ):
            operation = self.token
            self.advance()
            right_node = self.term()
            left_node = [left_node, operation, right_node]

        return left_node

    def if_statement(self):
        self.advance()
        condition = self.boolean_expression()

        if self.token != None:
            if self.token.value == DO:
                self.advance()
                action = self.statement()

                return condition, action
            elif (
                self.tokens[self.idx - 1].value != None
                and self.tokens[self.idx - 1].value == DO
            ):
                action = self.statement()

                return condition, action

    def if_statements(self) -> list | None:
        conditions = []
        actions = []
        if_statement = self.if_statement()

        if self.token != None and if_statement != None:
            conditions.append(if_statement[0])
            actions.append(if_statement[1])

            while self.token.value == ELIF:
                if_statement = self.if_statement()
                if if_statement != None:
                    conditions.append(if_statement[0])
                    actions.append(if_statement[1])

            if self.token.value == ELSE:
                self.advance()
                self.advance()
                else_action = self.statement()

                return [conditions, actions, else_action]

            return [conditions, actions]

    def while_statement(self):
        self.advance()
        condition = self.boolean_expression()

        if self.token != None:
            if self.token.value == DO:
                self.advance()
                action = self.statement()

                return condition, action
            elif (
                self.tokens[self.idx - 1].value != None
                and self.tokens[self.idx - 1].value == DO
            ):
                action = self.statement()

                return condition, action

    def comparison_expression(self) -> list[Token] | Token | None:
        left_node = self.expression()

        while self.token != None and (self.token.type == COMPARISON):
            operation = self.token
            self.advance()
            right_node = self.expression()
            left_node = [left_node, operation, right_node]

        return left_node

    def boolean_expression(self) -> list[Token] | Token | None:
        left_node = self.comparison_expression()

        while self.token != None and (self.token.type == BOOLEAN):
            operation = self.token
            self.advance()
            right_node = self.comparison_expression()
            left_node = [left_node, operation, right_node]

        return left_node

    def statement(self) -> list | Token | None:
        if self.token != None:
            if self.token.type == DECLARATION:
                # Variable assignment
                self.advance()
                left_node = self.variable()
                self.advance()
                if self.token.value == "=":
                    operation = self.token
                    self.advance()
                    right_node = self.boolean_expression()
                    return [left_node, operation, right_node]
            elif (
                self.token.type == INTEGER
                or self.token.type == FLOAT
                or self.token.value == OPERATION
                or self.token.value == PLUS
                or self.token.value == MINUS
                or self.token.value == "("
                or self.token.value == NOT
            ):
                # Arithmetic expression
                return self.boolean_expression()
            elif self.token.value == IF:
                return [self.token, self.if_statements()]
            elif self.token.value == WHILE:
                return [self.token, self.while_statement()]

    def parse(self) -> list[Token] | Token | None:
        return self.statement()

    def advance(self) -> None:
        self.idx += 1
        if self.idx < len(self.tokens):
            self.token = self.tokens[self.idx]

    def variable(self) -> Token | None:
        if self.token != None:
            if self.token.type.startswith(VARIABLE):
                return self.token
