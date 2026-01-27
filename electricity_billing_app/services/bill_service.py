"""
Bill Service Module
-------------------
Manages bill creation and calculations with validation.

Module: bill_service.py
Purpose: Create bills with validation, previous dues, and fine calculation
Input: Bill data dictionaries
Output: Created bill documents
Author: Software Engineering Lab
Date: 2026-01-27
"""

from datetime import datetime, timedelta
from bson.objectid import ObjectId
from decimal import Decimal
from services.tariff_service import TariffService
from modules.validation import validate_units
from modules.constants import DUE_DATE_DAYS, FINE_AMOUNT, ERROR_MESSAGES


class BillService:
    def __init__(self, db):
        self.bills_collection = db['electricity_billing']
        self.households_collection = db['households']

    def create_bill(self, data):
        """
        Create a new bill with validation and calculations.
        
        Preconditions:
        - data contains required keys: household_id or service_number, units
        - Database collections are properly initialized
        
        Logic:
        1. Validate input data (units must be non-negative)
        2. Find household by ID or service number
        3. Calculate current charges using TariffService
        4. Query previous unpaid bills for this household
        5. Calculate fine if applicable
        6. Calculate total amount = current + previous dues + fine
        7. Set due date = bill date + 15 days
        8. Create and insert bill document
        9. Return created bill
        
        Algorithm:
        ----------
        VALIDATE units (must be >= 0)
        
        FIND household in database
        IF household not found:
            RAISE error
        
        current_charges = TariffService.calculate_bill(units)
        
        previous_bills = QUERY unpaid bills for this household
        previous_dues = SUM of all previous_bills.total_amount
        
        fine = data.get('fine_amount', 0)
        total = current_charges + previous_dues + fine
        
        due_date = today + 15 days
        
        CREATE bill_document with all fields
        INSERT into database
        RETURN bill_document
        
        Input:
        - data (dict): {
            'household_id': str (ObjectId) OR 'service_number': str,
            'units': float,
            'fine_amount': float (optional),
            'notes': str (optional)
          }
        
        Output:
        - dict: Created bill document with all fields
        
        Raises:
        - ValueError: If validation fails or household not found
        
        Examples:
        >>> bill_service.create_bill({'household_id': '...', 'units': 100})
        # Returns complete bill document
        """
        # Extract and validate units
        units = data.get('units', 0)
        is_valid, error_msg = validate_units(units)
        if not is_valid:
            raise ValueError(error_msg)
        
        units = Decimal(str(units))
        fine_amount = Decimal(str(data.get('fine_amount', 0)))
        
        # Find household by ID or service number
        household = None
        if 'household_id' in data:
            household_id = data['household_id']
            household = self.households_collection.find_one({"_id": ObjectId(household_id)})
        elif 'service_number' in data:
            service_number = data['service_number']
            household = self.households_collection.find_one({"service_number": service_number})
        
        if not household:
            raise ValueError(ERROR_MESSAGES['household_not_found'])
        
        household_id = household['_id']
        connection_type = household.get('connection_type', 'Household')
        service_number = household.get('service_number', household.get('house_number', 'N/A'))
        
        # Calculate Current Charges using new tariff service
        tariff_result = TariffService.calculate_bill(float(units))
        current_charges = Decimal(str(tariff_result['base_amount']))
        breakdown = tariff_result['breakdown']
        minimum_charge_applied = tariff_result['minimum_charge_applied']
        
        # Calculate Previous Dues
        # Query all unpaid bills for this household
        previous_unpaid_bills = self.bills_collection.find({
            "household_id": household_id,
            "status": "Unpaid",
            "_id": {"$exists": True}  # Ensure we don't count the bill we're creating
        })
        
        previous_dues = Decimal('0.00')
        for prev_bill in previous_unpaid_bills:
            previous_dues += Decimal(str(prev_bill.get('total_amount', 0)))
        
        # Calculate Total
        total_amount = current_charges + fine_amount + previous_dues
        
        # Calculate due date (15 days from today)
        bill_date = datetime.now()
        due_date = bill_date + timedelta(days=DUE_DATE_DAYS)
        
        # Create bill document
        bill_document = {
            "household_id": ObjectId(household_id),
            "household_name": household.get('household_name'),
            "service_number": service_number,
            "house_number": household.get('house_number'),
            "address": household.get('address', 'N/A'),
            "phone": household.get('phone', 'N/A'),
            "connection_type": connection_type,
            "units": float(units),
            "rate_breakdown": {
                "base_amount": float(current_charges),
                "fine_amount": float(fine_amount),
                "previous_dues": float(previous_dues),
                "slab_breakdown": breakdown,
                "minimum_charge_applied": minimum_charge_applied
            },
            "total_amount": float(total_amount),
            "date": bill_date,
            "due_date": due_date,
            "status": "Unpaid",
            "notes": data.get('notes', '')
        }
        
        # Insert into database
        result = self.bills_collection.insert_one(bill_document)
        bill_document['_id'] = result.inserted_id
        
        return bill_document
    
    def get_bill_by_service_number(self, service_number):
        """
        Retrieve all bills for a given service number.
        
        Input:
        - service_number (str): Service number to search for
        
        Output:
        - list: List of bill documents
        """
        return list(self.bills_collection.find(
            {"service_number": service_number}
        ).sort("date", -1))
    
    def mark_bill_paid(self, bill_id):
        """
        Mark a bill as paid.
        
        Input:
        - bill_id (str): Bill ID to mark as paid
        
        Output:
        - bool: True if successful, False otherwise
        """
        try:
            result = self.bills_collection.update_one(
                {"_id": ObjectId(bill_id)},
                {"$set": {"status": "Paid", "paid_date": datetime.now()}}
            )
            return result.modified_count > 0
        except Exception:
            return False

