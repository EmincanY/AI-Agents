from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import string
import random

class PasswordInput(BaseModel):
    length: int = Field(default=12, description="Length of the password to generate")
    include_special: bool = Field(default=True, description="Include special characters in the password")
    include_numbers: bool = Field(default=True, description="Include numbers in the password")

class PasswordTool(BaseTool):
    name: str = "generate_password"
    description: str = "Generate a secure random password"
    args_schema: Type[BaseModel] = PasswordInput

    def _run(self, length: int = 12, include_special: bool = True, include_numbers: bool = True) -> str:
        """Generate a secure random password."""
        try:
            if length < 8:
                return "Password length must be at least 8 characters"
            
            # Define character sets
            chars = string.ascii_letters
            if include_numbers:
                chars += string.digits
            if include_special:
                chars += string.punctuation
            
            # Generate password
            password = ''.join(random.choice(chars) for _ in range(length))
            
            # Ensure password contains at least one character from each required set
            if include_numbers and not any(c.isdigit() for c in password):
                password = password[:-1] + random.choice(string.digits)
            if include_special and not any(c in string.punctuation for c in password):
                password = password[:-1] + random.choice(string.punctuation)
            
            return f"Generated password ({length} characters):\n{password}"
        except Exception as e:
            return f"Error generating password: {str(e)}"

    async def _arun(self, length: int = 12, include_special: bool = True, include_numbers: bool = True) -> str:
        """Async implementation of password generation"""
        return self._run(length, include_special, include_numbers) 