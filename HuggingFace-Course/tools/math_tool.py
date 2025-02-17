from smolagents import tool
import sympy

@tool
def solve_math_expression(expression: str) -> str:
    """Solve a mathematical expression
    Args:
        expression: Mathematical expression as string
    """
    try:
        # Convert string to sympy expression
        expr = sympy.sympify(expression)
        result = expr.evalf()
        return f"Result: {result}"
    except Exception as e:
        return f"Error solving expression: {str(e)}" 