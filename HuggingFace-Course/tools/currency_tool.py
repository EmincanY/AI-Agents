from smolagents import tool
import requests

@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount from one currency to another
    Args:
        amount: Amount to convert
        from_currency: Source currency code (e.g., USD)
        to_currency: Target currency code (e.g., EUR)
    """
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