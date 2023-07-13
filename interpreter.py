from constants import (
    AND,
    DIVIDE,
    EQUAL,
    FLOAT,
    IF,
    INTEGER,
    MINUS,
    MULTIPLY,
    NOT,
    OR,
    PLUS,
    VARIABLE,
    WHILE,
)
from data import Data
from tokens import Boolean, Float, Integer, Reserved, Token


class Interpreter:
    def __init__(self, tree: list[Token] | Token | None, base: Data):
        self.tree = tree
        self.data = base

    def read_INTEGER(self, value: str | int | float) -> int:
        return int(value)

    def read_FLOAT(self, value: str | int | float) -> float:
        return float(value)

    def read_VARIABLE(self, id: str | int | float) -> Token | None:
        if isinstance(id, str):
            variable = self.data.read(id)
            variable_type = variable.type

            return getattr(self, f"read_{variable_type}")(variable.value)

    def compute_binary(
        self, left_tree: Token, operator: Token, right_tree: Token
    ) -> Token | None:
        left_type = VARIABLE if left_tree.type.startswith(VARIABLE) else left_tree.type
        right_type = (
            VARIABLE if right_tree.type.startswith(VARIABLE) else right_tree.type
        )

        left: int | float
        right: int | float

        if operator.value == EQUAL:
            left_tree.type = f"{VARIABLE}({right_type})"
            self.data.write(left_tree, right_tree)
            # return self.data.read_all()
            if isinstance(left_tree.value, str):
                return self.data.read(left_tree.value)

        left = getattr(self, f"read_{left_type}")(left_tree.value)
        right = getattr(self, f"read_{right_type}")(right_tree.value)

        output: int | float | None = None

        if operator.value == PLUS:
            output = left + right
        elif operator.value == MINUS:
            output = left - right
        elif operator.value == MULTIPLY:
            output = left * right
        elif operator.value == DIVIDE:
            output = left / right
        elif operator.value == ">":
            output = 1 if left > right else 0
        elif operator.value == "<":
            output = 1 if left < right else 0
        elif operator.value == ">=":
            output = 1 if left >= right else 0
        elif operator.value == "<=":
            output = 1 if left <= right else 0
        elif operator.value == "?=":
            output = 1 if left == right else 0
        elif operator.value == "!=":
            output = 1 if left != right else 0
        elif operator.value == AND:
            output = 1 if left and right else 0
        elif operator.value == OR:
            output = 1 if left or right else 0

        if output == None:
            return None

        return (
            Float(output)
            if (left_tree.type == FLOAT or right_tree.type == FLOAT)
            else Integer(output)
        )

    def compute_unary(self, operator: Token, operand: Token) -> Token | None:
        operand_type = VARIABLE if operand.type.startswith(VARIABLE) else operand.type

        operand_type: str

        if isinstance(operand.value, str):
            operand_value = getattr(self, f"read_{operand_type}")(operand.value)
            if operator.value == PLUS:
                return (
                    Integer(+operand_value)
                    if operand.type == INTEGER
                    else Float(+operand_value)
                )
            elif operator.value == MINUS:
                return (
                    Integer(-operand_value)
                    if operand.type == INTEGER
                    else Float(-operand_value)
                )
        elif operator.value == NOT:
            operand_value = getattr(self, f"read_{operand_type}")(operand.value)

            return Boolean(1 if not operand_value else 0)

    def interpret(self, tree: list[Token] | Token | None = None) -> Token | None:
        if tree is None:
            tree = self.tree

        if isinstance(tree, list):
            if isinstance(tree[0], Reserved):
                if not isinstance(tree[1], Token):
                    if tree[0].value == IF:
                        for idx, condition in enumerate(tree[1][0]):
                            evaluation = self.interpret(condition)
                            if evaluation != None:
                                if evaluation.value == 1:
                                    return self.interpret(tree[1][1][idx])

                        if len(tree[1]) == 3:
                            return self.interpret(tree[1][2])

                        else:
                            return None
                    elif tree[0].value == WHILE:
                        condition = self.interpret(tree[1][0])
                        while condition != None and condition.value == 1:
                            # Do action
                            print(self.interpret(tree[1][1]))

                            # Check condition
                            condition = self.interpret(tree[1][0])

                        return

        # Unary operation
        if isinstance(tree, list) and len(tree) == 2:
            exprission = tree[1]
            if isinstance(exprission, list):
                exprission = self.interpret(exprission)
            if exprission != None:
                return self.compute_unary(tree[0], exprission)

        # No operation
        elif isinstance(tree, Token):
            return tree

        elif tree != None:
            # Evaluate the left tree
            left_tree = tree[0]
            if isinstance(left_tree, list):
                left_tree = self.interpret(left_tree)

            operator = tree[1]

            # Evaluate the right tree
            right_tree = tree[2]
            if isinstance(right_tree, list):
                right_tree = self.interpret(right_tree)

            if left_tree == None or operator == None or right_tree == None:
                return None

            return self.compute_binary(left_tree, operator, right_tree)
