# src/utils/data_formatters.py

def format_currency(amount: float, currency: str = "USD") -> str:
    """Format a number as currency."""
    return f"{currency} {amount:,.2f}"

def format_percentage(value: float) -> str:
    """Format a number as a percentage."""
    return f"{value:.2f}%"
