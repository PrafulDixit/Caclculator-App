"""Safe arithmetic expression evaluator.
Supports: +, -, *, /, **, parentheses, unary - and numeric constants.
Uses Python's AST and whitelists node types.
"""
import ast
import operator as _op
from typing import Union

_ops = {
    ast.Add: _op.add,
    ast.Sub: _op.sub,
    ast.Mult: _op.mul,
    ast.Div: _op.truediv,
    ast.Pow: _op.pow,
}


def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant")
    # `ast.Num` was removed in some Python versions; handle it if present.
    if hasattr(ast, "Num") and isinstance(node, ast.Num):
        return node.n
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ops:
            return _ops[op_type](left, right)
        raise ValueError("Unsupported binary operator")
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return -_eval(node.operand)
        if isinstance(node.op, ast.UAdd):
            return _eval(node.operand)
        raise ValueError("Unsupported unary operator")
    raise ValueError("Unsupported expression")


def evaluate(expr: str) -> Union[int, float]:
    """Evaluate an arithmetic expression safely and return a number.

    Example: evaluate("2*(3+4) - 5/2") -> 11.5
    """
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ValueError("Invalid expression") from e
    return _eval(parsed)
