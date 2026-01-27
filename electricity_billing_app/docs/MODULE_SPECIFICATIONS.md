# Module Specifications
## Electricity Billing System - Lab Tasks 1 & 2

**Author**: Software Engineering Lab  
**Date**: 2026-01-27  
**Version**: 2.0.0

---

## Table of Contents

1. [Validation Module](#validation-module)
2. [Input Handler Module](#input-handler-module)
3. [Output Handler Module](#output-handler-module)
4. [Tariff Service Module](#tariff-service-module)
5. [Bill Service Module](#bill-service-module)

---

## Validation Module

### Function: `validate_consumer_name`

**Module**: `validation.py`

**Purpose**: Validate that consumer name contains only alphabetic characters and spaces (no numbers or special characters).

**Input Parameters**:
- `name` (str): The consumer/household name to validate

**Preconditions**:
- Input is a string (may be empty)

**Logic**:
```
**Logic**:
```
ALGORITHM: validate_consumer_name(name)
INPUT: name (string)
OUTPUT: (is_valid: boolean, error_message: string)

BEGIN
    IF name is None OR name is empty string THEN
        RETURN (False, "Name cannot be empty")
    END IF
    
    name = TRIM(name)  // Remove leading/trailing whitespace
    
    // Note: Application layer sanitizes name (lowercase, remove numbers) before calling this
    
    IF name matches pattern "^[A-Za-z\s]+$" THEN
        RETURN (True, "")
    ELSE
        RETURN (False, "Name must contain only alphabetic characters and spaces")
    END IF
END
```

**Output**:
- Tuple `(bool, str)`:
  - `(True, "")` if validation succeeds
  - `(False, error_message)` if validation fails

**Example Usage**:
```python
# Assuming pre-sanitization: "John123" -> "john"
is_valid, msg = validate_consumer_name("john")       # Returns (True, "")
is_valid, msg = validate_consumer_name("John@Doe")   # Returns (False, "Name must contain...")
is_valid, msg = validate_consumer_name("")           # Returns (False, "Name cannot be empty")
```

---

### Function: `validate_phone_number`

**Module**: `validation.py`

**Purpose**: Validate that phone number is exactly 10 digits.

**Input Parameters**:
- `phone` (str): The phone number to validate

**Preconditions**:
- Input is a string

**Logic**:
```
ALGORITHM: validate_phone_number(phone)
INPUT: phone (string)
OUTPUT: (is_valid: boolean, error_message: string)

BEGIN
    IF phone is None OR phone is empty THEN
        RETURN (False, "Phone number must be exactly 10 digits")
    END IF
    
    phone = TRIM(phone)
    
    IF LENGTH(phone) ≠ 10 THEN
        RETURN (False, "Phone number must be exactly 10 digits")
    END IF
    
    IF phone matches pattern "^\d{10}$" THEN
        RETURN (True, "")
    ELSE
        RETURN (False, "Phone number must contain only digits")
    END IF
END
```

**Output**:
- Tuple `(bool, str)` indicating validation result

**Example Usage**:
```python
is_valid, msg = validate_phone_number("1234567890")  # Returns (True, "")
is_valid, msg = validate_phone_number("12345")       # Returns (False, "Phone number...")
```

---

### Function: `validate_consumer_number`

**Module**: `validation.py`

**Purpose**: Validate consumer number format (numeric) and check uniqueness in database.

**Input Parameters**:
- `consumer_num` (str): The consumer number to validate
- `db_collection` (Collection, optional): MongoDB collection for duplicate checking

**Preconditions**:
- `consumer_num` is a string
- `db_collection` is a valid MongoDB collection object or None

**Logic**:
```
ALGORITHM: validate_consumer_number(consumer_num, db_collection)
INPUT: consumer_num (string), db_collection (DatabaseCollection or None)
OUTPUT: (is_valid: boolean, error_message: string)

BEGIN
    IF consumer_num is None OR TRIM(consumer_num) is empty THEN
        RETURN (False, "Invalid consumer number format (must be numeric)")
    END IF
    
    consumer_num = TRIM(consumer_num)
    
    IF consumer_num does NOT match pattern "^\d+$" THEN
        RETURN (False, "Invalid consumer number format (must be numeric)")
    END IF
    
    IF db_collection is NOT None THEN
        existing = QUERY db_collection WHERE service_number = consumer_num
        
        IF existing record found THEN
            RETURN (False, "Consumer number already exists in the system")
        END IF
    END IF
    
    RETURN (True, "")
END
```

**Output**:
- Tuple `(bool, str)` with validation result and error message

---

### Function: `validate_units`

**Module**: `validation.py`

**Purpose**: Validate that units consumed is a non-negative number.

**Input Parameters**:
- `units` (float/int/str): Units consumed value

**Preconditions**:
- None (handles type conversion internally)

**Logic**:
```
ALGORITHM: validate_units(units)
INPUT: units (any type)
OUTPUT: (is_valid: boolean, error_message: string)

BEGIN
    TRY
        units_float = CONVERT units TO float
    CATCH ValueError THEN
        RETURN (False, "Units must be a valid number")
    END TRY
    
    IF units_float < 0 THEN
        RETURN (False, "Units consumed cannot be negative")
    END IF
    
    RETURN (True, "")
END
```

**Output**:
- Tuple `(bool, str)` with validation result

**Example Usage**:
```python
is_valid, msg = validate_units(100)      # Returns (True, "")
is_valid, msg = validate_units(-10)      # Returns (False, "Units cannot be negative")
is_valid, msg = validate_units("abc")    # Returns (False, "Units must be a valid number")
```

---

## Tariff Service Module

### Function: `TariffService.calculate_bill`

**Module**: `tariff_service.py`

**Purpose**: Calculate electricity bill based on tiered slab rates as per Lab Task 1 specifications.

**Input Parameters**:
- `units` (float): Number of units consumed

**Preconditions**:
- Units must be a non-negative number

**Logic**:

**Lab Task 1 Specification**:
- First 50 units: ₹1.5 per unit
- Next 50 units (51-100): ₹2.5 per unit
- Next 50 units (101-150): ₹3.5 per unit
- Above 150 units: ₹4.5 per unit
- Minimum charge: ₹25 when units = 0

```
ALGORITHM: calculate_bill(units)
INPUT: units (float)
OUTPUT: dictionary {base_amount, minimum_charge_applied, breakdown}

BEGIN
    // Special case: Zero consumption
    IF units = 0 THEN
        RETURN {
            base_amount: 25.0,
            minimum_charge_applied: True,
            breakdown: []
        }
    END IF
    
    total = 0
    remaining = units
    breakdown = []
    slab_start = 0
    
    // Define slab structure
    slabs = [(50, 1.5), (50, 2.5), (50, 3.5), (infinity, 4.5)]
    
    // Calculate for each slab
    FOR each (slab_limit, rate) IN slabs DO
        IF remaining <= 0 THEN
            BREAK
        END IF
        
        // Units in this slab
        slab_units = MIN(remaining, slab_limit)
        slab_amount = slab_units × rate
        
        // Accumulate total
        total = total + slab_amount
        
        // Add to breakdown
        slab_label = CREATE_SLAB_LABEL(slab_start, slab_limit)
        breakdown.APPEND({
            slab: slab_label,
            units: slab_units,
            rate: rate,
            amount: slab_amount
        })
        
        // Update remaining
        remaining = remaining - slab_units
        slab_start = slab_start + slab_limit
    END FOR
    
    RETURN {
        base_amount: total,
        minimum_charge_applied: False,
        breakdown: breakdown
    }
END
```

**Output**:
- Dictionary with keys:
  - `base_amount` (float): Total calculated amount
  - `minimum_charge_applied` (bool): Whether minimum charge was used
  - `breakdown` (list): Slab-wise breakdown with units, rate, and amount

**Example Calculations**:

| Units | Calculation | Total Amount |
|-------|-------------|--------------|
| 0 | Minimum charge | ₹25.00 |
| 50 | 50 × 1.5 | ₹75.00 |
| 100 | 50×1.5 + 50×2.5 | ₹200.00 |
| 150 | 50×1.5 + 50×2.5 + 50×3.5 | ₹375.00 |
| 200 | 50×1.5 + 50×2.5 + 50×3.5 + 50×4.5 | ₹600.00 |

---

## Bill Service Module

### Function: `BillService.create_bill`

**Module**: `bill_service.py`

**Purpose**: Create a new electricity bill with validation, previous dues calculation, and fine handling.

**Input Parameters**:
- `data` (dict): Dictionary containing:
  - `household_id` (str) OR `service_number` (str): Identifier
  - `units` (float): Units consumed
  - `fine_amount` (float, optional): Fine to apply
  - `notes` (str, optional): Additional notes

**Preconditions**:
- Database collections are initialized
- Household exists in database
- Units is non-negative

**Logic**:
```
ALGORITHM: create_bill(data)
INPUT: data (dictionary)
OUTPUT: bill_document (dictionary)

BEGIN
    // Step 1: Validate units
    units = data.GET('units')
    (is_valid, error) = VALIDATE_UNITS(units)
    IF NOT is_valid THEN
        RAISE ValidationError(error)
    END IF
    
    // Step 2: Find household
    IF data contains 'household_id' THEN
        household = FIND household BY _id
    ELSE IF data contains 'consumer_number' THEN
        household = FIND household BY service_number  // DB field is still service_number
    END IF
    
    IF household NOT found THEN
        RAISE ValueError("Household not found")
    END IF
    
    // Step 3: Calculate current charges
    tariff_result = CALCULATE_BILL(units)
    current_charges = tariff_result.base_amount
    
    // Step 4: Calculate previous dues
    unpaid_bills = QUERY bills WHERE household_id = household._id AND status = "Unpaid"
    previous_dues = SUM of all unpaid_bills.total_amount
    
    // Step 5: Calculate total
    fine_amount = data.GET('fine_amount', default=0)
    total_amount = current_charges + previous_dues + fine_amount
    
    // Step 6: Set due date
    bill_date = CURRENT_DATE()
    due_date = bill_date + 15 days
    
    // Step 7: Create bill document
    bill_document = {
        household_id: household._id,
        household_name: household.name,
        consumer_number: household.service_number,
        house_number: household.house_number,
        address: household.address,
        phone: household.phone,
        units: units,
        rate_breakdown: {
            base_amount: current_charges,
            fine_amount: fine_amount,
            previous_dues: previous_dues,
            slab_breakdown: tariff_result.breakdown
        },
        total_amount: total_amount,
        date: bill_date,
        due_date: due_date,
        status: "Unpaid"
    }
    
    // Step 8: Insert into database
    INSERT bill_document INTO bills_collection
    
    RETURN bill_document
END
```

**Output**:
- Complete bill document with all fields populated

**Postconditions**:
- New bill is inserted into database
- Bill has status "Unpaid"
- Due date is set to 15 days from bill date

---

## Output Handler Module

### Function: `format_bill_display`

**Module**: `output_handler.py`

**Purpose**: Format bill data for display/printing with all required fields from Lab Task 1.

**Input Parameters**:
- `bill_data` (dict): Complete bill document

**Preconditions**:
- `bill_data` contains all required fields

**Logic**:
```
ALGORITHM: format_bill_display(bill_data)
INPUT: bill_data (dictionary)
OUTPUT: formatted_string (string)

BEGIN
    // Extract all fields
    consumer_name = bill_data.GET('household_name')
    consumer_number = bill_data.GET('consumer_number') OR bill_data.GET('service_number')
    units = bill_data.GET('units')
    bill_date = FORMAT_DATE(bill_data.GET('date'))
    due_date = FORMAT_DATE(bill_data.GET('due_date'))
    current_charges = bill_data.GET('rate_breakdown').base_amount
    previous_dues = bill_data.GET('rate_breakdown').previous_dues
    total_amount = bill_data.GET('total_amount')
    fine_amount = bill_data.GET('rate_breakdown').fine_amount
    
    // Build formatted output
    output = CREATE_HEADER("ELECTRICITY BILL")
    output = output + "Bill Date: " + bill_date + "\n"
    output = output + "Consumer Number: " + consumer_number + "\n"
    output = output + SEPARATOR
    output = output + "Consumer Name: " + consumer_name + "\n"
    output = output + "Units Consumed: " + units + "\n"
    output = output + "Current Charges: ₹" + current_charges + "\n"
    
    IF previous_dues > 0 THEN
        output = output + "Previous Dues: ₹" + previous_dues + "\n"
    END IF
    
    output = output + "Total Amount: ₹" + total_amount + "\n"
    output = output + "Due Date: " + due_date + "\n"
    output = output + "Late Payment Fine: ₹150.00 (after " + due_date + ")\n"
    output = output + "Amount After Due: ₹" + (total_amount + 150) + "\n"
    
    RETURN output
END
```

**Output**:
- Formatted string ready for console display or printing

**Lab Task 1 Output Requirements** (✓ All Met):
- ✓ Consumer name
- ✓ Consumer number  
- ✓ Date
- ✓ Units consumed
- ✓ Previous pending bills
- ✓ Due date (without fine)
- ✓ Amount after due date (with ₹150 fine)

---

## Summary

All modules follow consistent patterns:
- **Clear input/output specifications**
- **Preconditions and postconditions documented**
- **Algorithms provided in pseudocode**
- **Example usage included**
- **Error handling specified**

This modular design ensures:
- **Usability**: Easy to understand and use
- **Efficiency**: Optimized algorithms
- **Reusability**: Functions can be used across applications
- **Maintainability**: Well-documented and organized
