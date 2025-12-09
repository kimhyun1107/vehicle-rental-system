import os
from typing import List, Dict, Any

def clear_screen() -> None:
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause() -> None:
    """Pause program execution and wait for the user to press Enter."""
    input("\nPress Enter to continue...")

def get_next_id(data_list: List[Dict[str, Any]], id_field: str) -> int:
    """
    Get the next ID for a given entity.
    
    Args:
        data_list (List[Dict[str, Any]]): List of existing data dictionaries.
        id_field (str): The key name of the ID field.

    Returns:
        int: The next available ID (starting from 1 if list is empty).
    """
    if not data_list:
        return 1
    max_id = max(item[id_field] for item in data_list)
    return max_id + 1

def validate_email(email: str) -> bool:
    """
    Simple email format validation.
    
    Args:
        email (str): Email string to validate.
    
    Returns:
        bool: True if email format seems valid, False otherwise.
    """
    return '@' in email and '.' in email.split('@')[1]

def validate_phone(phone: str) -> bool:
    """
    Simple phone number validation (digits only, at least 10 characters).
    
    Args:
        phone (str): Phone number string to validate.
    
    Returns:
        bool: True if valid, False otherwise.
    """
    return phone.isdigit() and len(phone) >= 10
