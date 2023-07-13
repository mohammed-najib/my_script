from constants import (
    BOOLEAN,
    COMPARISON,
    DECLARATION,
    FLOAT,
    INTEGER,
    OPERATION,
    RESERVED,
    VARIABLE,
)


class Token:
    def __init__(self, type: str, value: str | int | float) -> None:
        self.type = type
        self.value: str | int | float = value

    def __repr__(self) -> str:
        return str(self.value)


class Integer(Token):
    def __init__(self, value: str | int | float) -> None:
        super().__init__(INTEGER, value)


class Float(Token):
    def __init__(self, value: str | int | float) -> None:
        super().__init__(FLOAT, value)


class Operation(Token):
    def __init__(self, value: str) -> None:
        super().__init__(OPERATION, value)


class Declaration(Token):
    def __init__(self, value: str) -> None:
        super().__init__(DECLARATION, value)


class Variable(Token):
    def __init__(self, value: str) -> None:
        super().__init__(f"{VARIABLE}(?)", value)


class Boolean(Token):
    def __init__(self, value: str | int) -> None:
        super().__init__(BOOLEAN, value)


class Comparison(Token):
    def __init__(self, value: str) -> None:
        super().__init__(COMPARISON, value)


class Reserved(Token):
    def __init__(self, value: str) -> None:
        super().__init__(RESERVED, value)
