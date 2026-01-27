"""
Constants Module
-----------------
Stores all system-wide configuration constants for the electricity billing system.

Module: constants.py
Purpose: Centralized configuration management
Author: Software Engineering Lab
Date: 2026-01-27
"""

import re

# ==================================================================================
# TARIFF RATES (Lab Task 1 Specification)
# ==================================================================================

# Tiered slab structure: (units_in_slab, rate_per_unit)
# Format: Each tuple represents (number of units in this slab, rate per unit)
TARIFF_SLABS = [
    (50, 1.5),           # First 50 units: ₹1.5 per unit
    (50, 2.5),           # Next 50 units (51-100): ₹2.5 per unit
    (50, 3.5),           # Next 50 units (101-150): ₹3.5 per unit
    (float('inf'), 4.5)  # Above 150 units: ₹4.5 per unit
]

# ==================================================================================
# BILLING CHARGES
# ==================================================================================

MINIMUM_CHARGE = 25.0       # Minimum charge when units consumed = 0
FINE_AMOUNT = 150.0         # Fine amount after due date
DUE_DATE_DAYS = 15          # Number of days before bill is due

# ==================================================================================
# VALIDATION RULES
# ==================================================================================

# Name validation: Only alphabets and spaces allowed
NAME_PATTERN = r'^[A-Za-z\s]+$'
NAME_REGEX = re.compile(NAME_PATTERN)

# Phone number validation
PHONE_LENGTH = 10           # Exact length required
PHONE_PATTERN = r'^\d{10}$' # Exactly 10 digits
PHONE_REGEX = re.compile(PHONE_PATTERN)

# Consumer number format
CONSUMER_NUMBER_PATTERN = r'^\d+$'
CONSUMER_NUMBER_REGEX = re.compile(CONSUMER_NUMBER_PATTERN)
CONSUMER_NUMBER_LENGTH = 8   # Default length for auto-generation (e.g., 00000001)

# ==================================================================================
# ERROR MESSAGES
# ==================================================================================

ERROR_MESSAGES = {
    'name_invalid': 'Name must contain only alphabetic characters and spaces (no numbers or special characters)',
    'name_empty': 'Name cannot be empty',
    'phone_invalid': 'Phone number must be exactly 10 digits',
    'phone_invalid_chars': 'Phone number must contain only digits',
    'consumer_duplicate': 'Consumer number already exists in the system',
    'consumer_invalid': 'Invalid consumer number format (must be numeric)',
    'units_negative': 'Units consumed cannot be negative',
    'units_invalid': 'Units must be a valid number',
    'household_not_found': 'Household/Consumer not found',
    'database_error': 'Database operation failed'
}

# ==================================================================================
# SUCCESS MESSAGES
# ==================================================================================

SUCCESS_MESSAGES = {
    'bill_created': 'Bill generated successfully',
    'consumer_added': 'Consumer registered successfully',
    'payment_recorded': 'Payment recorded successfully'
}

# ==================================================================================
# DISPLAY FORMATS
# ==================================================================================

CURRENCY_SYMBOL = '₹'
DATE_FORMAT = '%d-%m-%Y'
DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S'
