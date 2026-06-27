"""
HTTP client functions for the FastAPI Strategy Pattern Calculator API. 
Each function maps to one FastAPI endpoint and returns plain Python 
data structures - no requests. Response objects leak into views.
"""
import requests 
from django.conf import settings

BASE = settings.CALCULATOR_API_BASE

def get_operations() -> list[str]:
    """Return a list of registered operation keys."""
    response = requests.get(f"{BASE}/operations", timeout=5)
    response.raise_for_status()

    return response.json()["operations"]

def compute(operation: str, a: float, b: float)-> dict:
    """
        send a computation request. 
        Returns a dict with keys: operation, symbol, a, b, result.
        Raises requests.HTTPError on 400/402/422.
    """
    response = requests.post(
        f"{BASE}/compute", 
        json={"operation": operation, "a": a, "b": b},
        timeout=5,
    )
    response.raise_for_status()

    return response.json()

def get_history() -> list[str]:
    """
        Return the list of past computation records.
    """
    response = requests.get(f"{BASE}/history", timeout=5)
    response.raise_for_status()

    return [entry["record"] for entry in response.json()["entries"]]

def clear_history() -> None:
    """Delete all history entries."""
    response = requests.delete(f"{BASE}/history", timeout=5)
    response.raise_for_status()

    

