"""
Validation Module
-----------------
Provides comprehensive input validation functions for the electricity billing system.

Module: validation.py
Purpose: Validate consumer names, phone numbers, service numbers, and units
Input: Various data types depending on validation function
Output: Tuple (bool, str) indicating validation result and error message
Author: Software Engineering Lab
Date: 2026-01-27

Module Specifications:
----------------------
All validation functions follow a consistent pattern:
- Input: Data to validate + optional database collection for uniqueness checks
- Output: Tuple (is_valid: bool, error_message: str)
- Return: (True, "") if valid, (False, "error description") if invalid
"""

import re
from typing import Tuple
from modules.constants import (
    NAME_REGEX, PHONE_REGEX, PHONE_LENGTH,
    CONSUMER_NUMBER_REGEX, ERROR_MESSAGES
)


def validate_consumer_name(name: str) -> Tuple[bool, str]:
    """
    Validate consumer/household name.
    
    Preconditions:
    - name is a string (may be empty)
    
    Logic:
    1. Check if name is empty or None
    2. Strip whitespace and check again
    3. Match against NAME_REGEX pattern (only alphabets and spaces)
    4. Return validation result
    
    Input:
    - name (str): Consumer name to validate
    
    Output:
    - Tuple (bool, str): (is_valid, error_message)
      - (True, "") if valid
      - (False, error_message) if invalid
    
    Examples:
    >>> validate_consumer_name("John Doe")
    (True, '')
    >>> validate_consumer_name("John123")
    (False, 'Name must contain only alphabetic characters and spaces...')
    >>> validate_consumer_name("")
    (False, 'Name cannot be empty')
    """
    # Check for empty or None
    if not name or not name.strip():
        return False, ERROR_MESSAGES['name_empty']
    
    # Remove leading/trailing whitespace
    name = name.strip()
    
    # Validate against pattern (alphabets and spaces only)
    if not NAME_REGEX.match(name):
        return False, ERROR_MESSAGES['name_invalid']
    
    return True, ""


def validate_phone_number(phone: str) -> Tuple[bool, str]:
    """
    Validate phone number.
    
    Preconditions:
    - phone is a string
    
    Logic:
    1. Check if phone is empty or None
    2. Strip whitespace
    3. Check if length is exactly 10
    4. Check if all characters are digits using regex
    5. Return validation result
    
    Input:
    - phone (str): Phone number to validate
    
    Output:
    - Tuple (bool, str): (is_valid, error_message)
      - (True, "") if valid (exactly 10 digits)
      - (False, error_message) if invalid
    
    Examples:
    >>> validate_phone_number("1234567890")
    (True, '')
    >>> validate_phone_number("12345")
    (False, 'Phone number must be exactly 10 digits')
    >>> validate_phone_number("12345abcde")
    (False, 'Phone number must contain only digits')
    """
    # Check for empty or None
    if not phone:
        return False, ERROR_MESSAGES['phone_invalid']
    
    # Remove whitespace
    phone = phone.strip()
    
    # Check length
    if len(phone) != PHONE_LENGTH:
        return False, ERROR_MESSAGES['phone_invalid']
    
    # Check if all digits using regex
    if not PHONE_REGEX.match(phone):
        return False, ERROR_MESSAGES['phone_invalid_chars']
    
    return True, ""


def validate_consumer_number(consumer_num: str, db_collection=None) -> Tuple[bool, str]:
    """
    Validate consumer number (numeric only) and check uniqueness in database.
    
    Preconditions:
    - consumer_num is a string
    - db_collection is a MongoDB collection object (optional)
    
    Logic:
    1. Check if consumer_num is empty
    2. Strip whitespace
    3. Check if numeric using regex
    4. If db_collection provided, check for duplicates
    5. Return validation result
    
    Input:
    - consumer_num (str): Consumer number to validate
    - db_collection (Collection, optional): MongoDB collection for uniqueness check
    
    Output:
    - Tuple (bool, str): (is_valid, error_message)
      - (True, "") if valid and unique
      - (False, error_message) if invalid or duplicate
    """
    # Check for empty
    if not consumer_num or not consumer_num.strip():
        return False, ERROR_MESSAGES['consumer_invalid']
    
    consumer_num = consumer_num.strip()
    
    # Check if numeric
    if not CONSUMER_NUMBER_REGEX.match(consumer_num):
        return False, ERROR_MESSAGES['consumer_invalid']
    
    # Check uniqueness in database if collection provided
    if db_collection is not None:
        try:
            existing = db_collection.find_one({
                "service_number": consumer_num
            })
            
            if existing:
                return False, ERROR_MESSAGES['consumer_duplicate']
        except Exception as e:
            return False, f"{ERROR_MESSAGES['database_error']}: {str(e)}"
    
    return True, ""


def validate_units(units) -> Tuple[bool, str]:
    """
    Validate units consumed.
    
    Preconditions:
    - units can be string, int, or float
    
    Logic:
    1. Try to convert units to float
    2. Check if value is non-negative
    3. Return validation result
    
    Input:
    - units (str/int/float): Units consumed to validate
    
    Output:
    - Tuple (bool, str): (is_valid, error_message)
      - (True, "") if valid (non-negative number)
      - (False, error_message) if invalid
    
    Examples:
    >>> validate_units(100)
    (True, '')
    >>> validate_units("50.5")
    (True, '')
    >>> validate_units(-10)
    (False, 'Units consumed cannot be negative')
    >>> validate_units("invalid")
    (False, 'Units must be a valid number')
    """
    # Try to convert to float
    try:
        units_float = float(units)
    except (ValueError, TypeError):
        return False, ERROR_MESSAGES['units_invalid']
    
    # Check non-negative
    if units_float < 0:
        return False, ERROR_MESSAGES['units_negative']
    
    return True, ""


def validate_all_consumer_data(name: str, phone: str, consumer_num: str, 
                               db_collection=None) -> Tuple[bool, dict]:
    """
    Validate all consumer data at once.
    
    Preconditions:
    - All inputs are strings
    - db_collection is optional MongoDB collection
    
    Logic:
    1. Validate name
    2. Validate phone
    3. Validate consumer number
    4. Collect all errors
    5. Return overall result and error dictionary
    
    Input:
    - name (str): Consumer name
    - phone (str): Phone number
    - consumer_num (str): Consumer number
    - db_collection (Collection, optional): For uniqueness check
    
    Output:
    - Tuple (bool, dict): (all_valid, errors_dict)
      - (True, {}) if all valid
      - (False, {'field': 'error', ...}) if any invalid
    """
    errors = {}
    
    # Validate name
    name_valid, name_error = validate_consumer_name(name)
    if not name_valid:
        errors['name'] = name_error
    
    # Validate phone
    phone_valid, phone_error = validate_phone_number(phone)
    if not phone_valid:
        errors['phone'] = phone_error
    
    # Validate consumer number
    consumer_valid, consumer_error = validate_consumer_number(consumer_num, db_collection)
    if not consumer_valid:
        errors['consumer_number'] = consumer_error
    
    # Return overall result
    all_valid = len(errors) == 0
    return all_valid, errors
