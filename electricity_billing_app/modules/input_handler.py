"""
Input Handler Module
--------------------
Handles user input collection with validation and re-prompting.

Module: input_handler.py
Purpose: Collect and validate user inputs with error handling
Input: Prompts and validator functions
Output: Validated user data
Author: Software Engineering Lab
Date: 2026-01-27

Module Specifications:
----------------------
This module provides generic input collection functions that:
- Display prompts to users
- Collect input
- Validate using provided validator functions
- Re-prompt on validation errors
- Return validated data
"""

from typing import Callable, Any, Tuple
from modules.validation import validate_all_consumer_data


def get_validated_input(prompt: str, validator_func: Callable, 
                       *validator_args, **validator_kwargs) -> str:
    """
    Get validated input from user with re-prompting on errors.
    
    Preconditions:
    - prompt is a non-empty string
    - validator_func is a callable that returns Tuple[bool, str]
    
    Logic:
    1. Display prompt to user
    2. Read input
    3. Call validator_func with input and additional args
    4. If validation fails, display error and re-prompt
    5. If validation succeeds, return validated input
    6. Repeat until valid input received
    
    Input:
    - prompt (str): Message to display to user
    - validator_func (Callable): Function that validates input
    - *validator_args: Additional arguments for validator
    - **validator_kwargs: Additional keyword arguments for validator
    
    Output:
    - str: Validated user input
    
    Examples:
    >>> # This would prompt user until valid name entered
    >>> name = get_validated_input("Enter name: ", validate_consumer_name)
    >>> # This would prompt for phone
    >>> phone = get_validated_input("Enter phone: ", validate_phone_number)
    """
    while True:
        user_input = input(prompt).strip()
        
        # Call validator function
        is_valid, error_message = validator_func(user_input, *validator_args, **validator_kwargs)
        
        if is_valid:
            return user_input
        else:
            print(f"❌ Error: {error_message}")
            print("   Please try again.\n")


def collect_consumer_details(db_collection=None) -> dict:
    """
    Collect all consumer details with validation.
    
    Preconditions:
    - db_collection is optional MongoDB collection for duplicate checking
    
    Logic:
    1. Prompt for consumer name (validate: alphabets only)
    2. Prompt for phone number (validate: exactly 10 digits)
    3. Prompt for service number (validate: uniqueness if db provided)
    4. Prompt for house number
    5. Prompt for address
    6. Return dictionary of collected data
    
    Input:
    - db_collection (Collection, optional): MongoDB collection for validation
    
    Output:
    - dict: Dictionary containing all consumer details
      {
          'household_name': str,
          'phone': str,
          'service_number': str,
          'house_number': str,
          'address': str
      }
    
    Examples:
    >>> details = collect_consumer_details()
    >>> # Returns: {'household_name': 'John Doe', 'phone': '1234567890', ...}
    """
    from modules.validation import (
        validate_consumer_name, 
        validate_phone_number, 
        validate_service_number
    )
    
    print("\n" + "="*60)
    print("  CONSUMER REGISTRATION")
    print("="*60 + "\n")
    
    # Collect consumer name
    household_name = get_validated_input(
        "Enter consumer name (alphabets only): ",
        validate_consumer_name
    )
    
    # Collect phone number
    phone = get_validated_input(
        "Enter phone number (10 digits): ",
        validate_phone_number
    )
    
    # Collect consumer number
    consumer_number = get_validated_input(
        "Enter consumer number (numeric only): ",
        validate_consumer_number,
        db_collection
    )
    
    # Collect house number (no strict validation needed)
    house_number = input("Enter house number: ").strip()
    
    # Collect address
    address = input("Enter address: ").strip()
    
    print("\n✅ All details collected successfully!\n")
    
    return {
        'household_name': household_name,
        'phone': phone,
        'consumer_number': consumer_number,
        'house_number': house_number,
        'address': address
    }


def collect_bill_details() -> dict:
    """
    Collect bill generation details with validation.
    
    Preconditions:
    - None
    
    Logic:
    1. Prompt for service number
    2. Prompt for units consumed (validate: non-negative number)
    3. Return dictionary of collected data
    
    Input:
    - None
    
    Output:
    - dict: Dictionary containing bill details
      {
          'service_number': str,
          'units': float
      }
    
    Examples:
    >>> bill_data = collect_bill_details()
    >>> # Returns: {'service_number': 'SVC001', 'units': 150.5}
    """
    from modules.validation import validate_units
    
    print("\n" + "="*60)
    print("  BILL GENERATION")
    print("="*60 + "\n")
    
    # Collect consumer number
    consumer_number = input("Enter consumer number: ").strip()
    
    # Collect units with validation
    units_str = get_validated_input(
        "Enter units consumed: ",
        validate_units
    )
    
    units = float(units_str)
    
    return {
        'consumer_number': consumer_number,
        'units': units
    }
