"""
Output Handler Module
---------------------
Handles formatting and display of bills and reports.

Module: output_handler.py
Purpose: Format and display bill information
Input: Bill data dictionaries
Output: Formatted strings for display/printing
Author: Software Engineering Lab
Date: 2026-01-27

Module Specifications:
----------------------
This module provides output formatting functions for:
- Console bill display
- Detailed bill breakdown
- Summary reports
"""

from datetime import datetime
from typing import Dict, List
from modules.constants import CURRENCY_SYMBOL, DATE_FORMAT


def format_bill_display(bill_data: dict) -> str:
    """
    Format bill data for display.
    
    Preconditions:
    - bill_data is a dictionary containing bill information
    
    Logic:
    1. Extract all relevant fields from bill_data
    2. Format currency amounts with symbol
    3. Format dates
    4. Create formatted string with proper alignment
    5. Return formatted bill
    
    Input:
    - bill_data (dict): Dictionary containing bill information
      Required keys: household_name, service_number, house_number, date,
                    units, rate_breakdown, total_amount, due_date
    
    Output:
    - str: Formatted bill string ready for display/printing
    
    Examples:
    >>> bill = {'household_name': 'John Doe', 'units': 100, ...}
    >>> print(format_bill_display(bill))
    # Displays formatted bill
    """
    # Extract data
    consumer_name = bill_data.get('household_name', 'N/A')
    consumer_number = bill_data.get('service_number', bill_data.get('house_number', 'N/A'))
    house_number = bill_data.get('house_number', 'N/A')
    address = bill_data.get('address', 'N/A')
    
    # Date handling
    bill_date = bill_data.get('date', datetime.now())
    if isinstance(bill_date, datetime):
        bill_date_str = bill_date.strftime(DATE_FORMAT)
    else:
        bill_date_str = str(bill_date)
    
    due_date = bill_data.get('due_date', datetime.now())
    if isinstance(due_date, datetime):
        due_date_str = due_date.strftime(DATE_FORMAT)
    else:
        due_date_str = str(due_date)
    
    # Units and amounts
    units = bill_data.get('units', 0)
    rate_breakdown = bill_data.get('rate_breakdown', {})
    base_amount = rate_breakdown.get('base_amount', 0)
    fine_amount = rate_breakdown.get('fine_amount', 0)
    previous_dues = rate_breakdown.get('previous_dues', 0)
    total_amount = bill_data.get('total_amount', 0)
    total_with_fine = total_amount + fine_amount if fine_amount == 0 else total_amount
    
    # Build formatted output
    output = []
    output.append("\n" + "="*70)
    output.append("                    ELECTRICITY BILL")
    output.append("="*70)
    output.append("")
    output.append(f"Bill Date         : {bill_date_str}")
    output.append(f"Consumer Number   : {consumer_number}")
    output.append("")
    output.append("-" * 70)
    output.append("CONSUMER DETAILS")
    output.append("-" * 70)
    output.append(f"Name              : {consumer_name}")
    output.append(f"House Number      : {house_number}")
    output.append(f"Address           : {address}")
    output.append("")
    output.append("-" * 70)
    output.append("BILLING DETAILS")
    output.append("-" * 70)
    output.append(f"Units Consumed    : {units:.2f} units")
    output.append(f"Current Charges   : {CURRENCY_SYMBOL}{base_amount:.2f}")
    
    if previous_dues > 0:
        output.append(f"Previous Dues     : {CURRENCY_SYMBOL}{previous_dues:.2f}")
    
    output.append("")
    output.append(f"Total Amount      : {CURRENCY_SYMBOL}{total_amount:.2f}")
    output.append(f"Due Date          : {due_date_str}")
    output.append("")
    
    if fine_amount > 0:
        output.append(f"⚠️  OVERDUE - Fine Applied: {CURRENCY_SYMBOL}{fine_amount:.2f}")
        output.append(f"Amount After Due  : {CURRENCY_SYMBOL}{total_with_fine:.2f}")
    else:
        output.append(f"Late Payment Fine : {CURRENCY_SYMBOL}150.00 (after {due_date_str})")
        output.append(f"Amount After Due  : {CURRENCY_SYMBOL}{total_amount + 150:.2f}")
    
    output.append("")
    output.append("="*70)
    output.append("          Thank you for your prompt payment!")
    output.append("="*70 + "\n")
    
    return "\n".join(output)


def format_bill_breakdown(breakdown_list: List[dict]) -> str:
    """
    Format detailed slab-wise bill breakdown.
    
    Preconditions:
    - breakdown_list is a list of dictionaries with slab details
    
    Logic:
    1. Create table header
    2. For each slab, format units, rate, and amount
    3. Align columns properly
    4. Add total row
    5. Return formatted table
    
    Input:
    - breakdown_list (list): List of slab breakdown dictionaries
      Each dict: {'slab': str, 'units': float, 'rate': float, 'amount': float}
    
    Output:
    - str: Formatted breakdown table
    
    Examples:
    >>> breakdown = [{'slab': '0-50', 'units': 50, 'rate': 1.5, 'amount': 75}]
    >>> print(format_bill_breakdown(breakdown))
    # Displays formatted breakdown table
    """
    if not breakdown_list:
        return "No breakdown available"
    
    output = []
    output.append("\n" + "-" * 70)
    output.append("DETAILED BREAKDOWN")
    output.append("-" * 70)
    output.append(f"{'Slab':<15} {'Units':<15} {'Rate':<15} {'Amount':<15}")
    output.append("-" * 70)
    
    total = 0
    for item in breakdown_list:
        slab = item.get('slab', 'N/A')
        units = item.get('units', 0)
        rate = item.get('rate', 0)
        amount = item.get('amount', 0)
        total += amount
        
        output.append(
            f"{slab:<15} {units:<15.2f} "
            f"{CURRENCY_SYMBOL}{rate:<14.2f} {CURRENCY_SYMBOL}{amount:<14.2f}"
        )
    
    output.append("-" * 70)
    output.append(f"{'TOTAL':<15} {'':<15} {'':<15} {CURRENCY_SYMBOL}{total:<14.2f}")
    output.append("-" * 70 + "\n")
    
    return "\n".join(output)


def format_summary_report(bills_list: List[dict]) -> str:
    """
    Format summary report for multiple bills.
    
    Preconditions:
    - bills_list is a list of bill dictionaries
    
    Logic:
    1. Count total bills
    2. Calculate total amount
    3. Calculate average consumption
    4. Format summary statistics
    5. Return formatted report
    
    Input:
    - bills_list (list): List of bill dictionaries
    
    Output:
    - str: Formatted summary report
    
    Examples:
    >>> bills = [{'units': 100, 'total_amount': 200}, ...]
    >>> print(format_summary_report(bills))
    # Displays summary statistics
    """
    if not bills_list:
        return "No bills found"
    
    total_bills = len(bills_list)
    total_units = sum(bill.get('units', 0) for bill in bills_list)
    total_amount = sum(bill.get('total_amount', 0) for bill in bills_list)
    avg_units = total_units / total_bills if total_bills > 0 else 0
    avg_amount = total_amount / total_bills if total_bills > 0 else 0
    
    output = []
    output.append("\n" + "="*60)
    output.append("                    SUMMARY REPORT")
    output.append("="*60)
    output.append(f"Total Bills       : {total_bills}")
    output.append(f"Total Units       : {total_units:.2f}")
    output.append(f"Total Amount      : {CURRENCY_SYMBOL}{total_amount:.2f}")
    output.append(f"Average Units     : {avg_units:.2f}")
    output.append(f"Average Amount    : {CURRENCY_SYMBOL}{avg_amount:.2f}")
    output.append("="*60 + "\n")
    
    return "\n".join(output)
