from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from sympy import sympify, SympifyError

class MathInput(BaseModel):
    expression: str = Field(description="The mathematical expression to evaluate")

class MathTool(BaseTool):
    name: str = "solve_math_expression"
    description: str = "Solve mathematical expressions and equations"
    args_schema: Type[BaseModel] = MathInput

    def _run(self, expression: str) -> str:
        """Evaluate a mathematical expression."""
        try:
            # Clean the expression
            expression = expression.replace('^', '**')
            
            # Evaluate using sympy
            result = sympify(expression)
            
            return f"Result of '{expression}':\n{result}"
        except SympifyError as e:
            return f"Invalid mathematical expression: {str(e)}"
        except Exception as e:
            return f"Error evaluating expression: {str(e)}"

    async def _arun(self, expression: str) -> str:
        """Async implementation of math expression evaluation"""
        return self._run(expression) 