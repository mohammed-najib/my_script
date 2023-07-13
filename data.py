from tokens import Token


class Data:
    def __init__(self) -> None:
        self.variables: dict[str, Token] = {}

    def read(self, id: str) -> Token:
        return self.variables[id]

    def read_all(self) -> dict[str, Token]:
        return self.variables

    def write(self, variable: Token, expression: Token) -> None:
        if isinstance(variable.value, str):
            variable_name = variable.value
            self.variables[variable_name] = expression
