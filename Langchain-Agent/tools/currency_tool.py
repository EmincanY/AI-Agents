from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests

class CurrencyInput(BaseModel):
    amount: float = Field(description="The amount to convert")
    from_currency: str = Field(description="The source currency code (e.g., USD, EUR)")
    to_currency: str = Field(description="The target currency code (e.g., USD, EUR)")

class CurrencyTool(BaseTool):
    name: str = "convert_currency"
    description: str = "Convert an amount from one currency to another using current exchange rates"
    args_schema: Type[BaseModel] = CurrencyInput

    def _run(self, amount: float, from_currency: str, to_currency: str) -> str:
        """Convert currency using current exchange rates."""
        try:
            # Using ExchangeRate-API
            base_url = "https://api.exchangerate-api.com/v4/latest"
            
            # Get exchange rates for the base currency
            response = requests.get(f"{base_url}/{from_currency.upper()}")
            data = response.json()
            
            if response.status_code == 200:
                # Get the exchange rate for the target currency
                if to_currency.upper() in data['rates']:
                    rate = data['rates'][to_currency.upper()]
                    converted_amount = amount * rate
                    return f"{amount} {from_currency.upper()} = {converted_amount:.2f} {to_currency.upper()} (Rate: 1 {from_currency.upper()} = {rate:.4f} {to_currency.upper()})"
                else:
                    return f"Error: Target currency {to_currency.upper()} not found"
            else:
                return f"Error: {data.get('error', 'Failed to fetch exchange rates')}"
        except Exception as e:
            return f"Error converting currency: {str(e)}"

    async def _arun(self, amount: float, from_currency: str, to_currency: str) -> str:
        """Async implementation of currency conversion"""
        return self._run(amount, from_currency, to_currency) 