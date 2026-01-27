# Test Plan
## Electricity Billing System - Lab Tasks 1 & 2

**Author**: Software Engineering Lab  
**Date**: 2026-01-27  
**Version**: 2.0.0

---

## 1. Validation Tests

### Test Cases for Name Validation

| Test ID | Functionality | Input | Expected Output | Actual Output | Status |
|---------|---------------|-------|-----------------|---------------|--------|
| VAL-001 | Valid name with alphabets only | "John Doe" | (True, "") | _To be filled_ | ⬜ Pending |
| VAL-002 | Name with numbers (Sanitization) | "John123" | (True, "") [Sanitized to "john"] | _To be filled_ | ⬜ Pending |
| VAL-003 | Invalid name with special characters | "John@Doe" | (False, "Name must contain only alphabetic...") | _To be filled_ | ⬜ Pending |
| VAL-004 | Empty name | "" | (False, "Name cannot be empty") | _To be filled_ | ⬜ Pending |
| VAL-005 | Whitespace-only name | "   " | (False, "Name cannot be empty") | _To be filled_ | ⬜ Pending |

### Test Cases for Phone Number Validation

| Test ID | Functionality | Input | Expected Output | Actual Output | Status |
|---------|---------------|-------|-----------------|---------------|--------|
| VAL-006 | Valid 10-digit phone | "1234567890" | (True, "") | _To be filled_ | ⬜ Pending |
| VAL-007 | Invalid phone - 9 digits | "123456789" | (False, "Phone number must be exactly 10 digits") | _To be filled_ | ⬜ Pending |
| VAL-008 | Invalid phone - 11 digits | "12345678901" | (False, "Phone number must be exactly 10 digits") | _To be filled_ | ⬜ Pending |
| VAL-009 | Invalid phone - contains letters | "12345abcde" | (False, "Phone number must contain only digits") | _To be filled_ | ⬜ Pending |
| VAL-010 | Empty phone | "" | (False, "Phone number must be exactly 10 digits") | _To be filled_ | ⬜ Pending |

### Test Cases for Consumer Number Validation

| Test ID | Functionality | Input (Consumer Number, DB) | Expected Output | Actual Output | Status |
|---------|---------------|----------------------------|-----------------|---------------|--------|
| VAL-011 | Valid consumer number (no DB check) | ("00000001", None) | (True, "") | _To be filled_ | ⬜ Pending |
| VAL-012 | Empty consumer number | ("", None) | (False, "Invalid consumer number format (must be numeric)") | _To be filled_ | ⬜ Pending |
| VAL-013 | Duplicate consumer number | ("00000001", mock_db with existing) | (False, "Consumer number already exists") | _To be filled_ | ⬜ Pending |
| VAL-013b | Invalid non-numeric consumer number | ("SVC001", None) | (False, "Invalid consumer number format (must be numeric)") | _To be filled_ | ⬜ Pending |

### Test Cases for Units Validation

| Test ID | Functionality | Input | Expected Output | Actual Output | Status |
|---------|---------------|-------|-----------------|---------------|--------|
| VAL-014 | Valid positive integer | 100 | (True, "") | _To be filled_ | ⬜ Pending |
| VAL-015 | Valid positive float | 50.5 | (True, "") | _To be filled_ | ⬜ Pending |
| VAL-016 | Valid zero units | 0 | (True, "") | _To be filled_ | ⬜ Pending |
| VAL-017 | Invalid negative units | -10 | (False, "Units consumed cannot be negative") | _To be filled_ | ⬜ Pending |
| VAL-018 | Invalid string | "invalid" | (False, "Units must be a valid number") | _To be filled_ | ⬜ Pending |

---

## 2. Tariff Calculation Tests

### Test Cases for Bill Calculation

| Test ID | Functionality | Units | Expected Amount | Calculation | Actual Output | Status |
|---------|---------------|-------|-----------------|-------------|---------------|--------|
| TARIFF-001 | Zero units (minimum charge) | 0 | ₹25.00 | Minimum charge | _To be filled_ | ⬜ Pending |
| TARIFF-002 | First slab only | 50 | ₹75.00 | 50 × 1.5 | _To be filled_ | ⬜ Pending |
| TARIFF-003 | Two slabs | 100 | ₹200.00 | 50×1.5 + 50×2.5 | _To be filled_ | ⬜ Pending |
| TARIFF-004 | Three slabs | 150 | ₹375.00 | 50×1.5 + 50×2.5 + 50×3.5 | _To be filled_ | ⬜ Pending |
| TARIFF-005 | Four slabs | 200 | ₹600.00 | 50×1.5 + 50×2.5 + 50×3.5 + 50×4.5 | _To be filled_ | ⬜ Pending |
| TARIFF-006 | Partial slab (25 units) | 25 | ₹37.50 | 25 × 1.5 | _To be filled_ | ⬜ Pending |
| TARIFF-007 | Partial slab (75 units) | 75 | ₹137.50 | 50×1.5 + 25×2.5 | _To be filled_ | ⬜ Pending |
| TARIFF-008 | Partial slab (175 units) | 175 | ₹487.50 | 50×1.5 + 50×2.5 + 50×3.5 + 25×4.5 | _To be filled_ | ⬜ Pending |
| TARIFF-009 | Large usage (500 units) | 500 | ₹1950.00 | 50×1.5 + 50×2.5 + 50×3.5 + 350×4.5 | _To be filled_ | ⬜ Pending |
| TARIFF-010 | Decimal units | 50.5 | ₹76.25 | 50×1.5 + 0.5×2.5 | _To be filled_ | ⬜ Pending |

### Test Cases for Minimum Charge

| Test ID | Functionality | Units | Expected Behavior | Actual Output | Status |
|---------|---------------|-------|-------------------|---------------|--------|
| MIN-001 | Zero units applies minimum | 0 | minimum_charge_applied = True, amount = 25 | _To be filled_ | ⬜ Pending |
| MIN-002 | Non-zero doesn't apply minimum | 10 | minimum_charge_applied = False, amount = 15 | _To be filled_ | ⬜ Pending |

---

## 3. Bill Service Tests

### Test Cases for Bill Creation

| Test ID | Functionality | Input Data | Expected Behavior | Actual Output | Status |
|---------|---------------|------------|-------------------|---------------|--------|
| BILL-001 | Create bill with valid data | {household_id: valid, units: 100} | Bill created with total ₹200 | _To be filled_ | ⬜ Pending |
| BILL-002 | Reject invalid household ID | {household_id: "invalid", units: 100} | Raises "Household not found" error | _To be filled_ | ⬜ Pending |
| BILL-003 | Reject negative units | {household_id: valid, units: -10} | Raises "Units cannot be negative" error | _To be filled_ | ⬜ Pending |
| BILL-004 | Calculate with previous dues | Consumer with ₹200 unpaid, units: 50 | New bill total = ₹75 + ₹200 = ₹275 | _To be filled_ | ⬜ Pending |
| BILL-005 | Set correct due date | {household_id: valid, units: 100} | due_date = bill_date + 15 days | _To be filled_ | ⬜ Pending |
| BILL-006 | Include breakdown in bill | {household_id: valid, units: 150} | rate_breakdown.slab_breakdown has 3 entries | _To be filled_ | ⬜ Pending |

---

## 4. Fine Calculation Tests

| Test ID | Functionality | Bill Date | Due Date | Payment Date | Expected Fine | Actual Output | Status |
|---------|---------------|-----------|----------|--------------|---------------|---------------|--------|
| FINE-001 | No fine before due date | 2026-01-01 | 2026-01-16 | 2026-01-10 | ₹0 | _To be filled_ | ⬜ Pending |
| FINE-002 | No fine on due date | 2026-01-01 | 2026-01-16 | 2026-01-16 | ₹0 | _To be filled_ | ⬜ Pending |
| FINE-003 | Fine after due date | 2026-01-01 | 2026-01-16 | 2026-01-20 | ₹150 | _To be filled_ | ⬜ Pending |

---

## 5. Previous Bills Tests

| Test ID | Functionality | Scenario | Expected Behavior | Actual Output | Status |
|---------|---------------|----------|-------------------|---------------|--------|
| PREV-001 | New customer (no previous dues) | First bill for household | previous_dues = 0 | _To be filled_ | ⬜ Pending |
| PREV-002 | Customer with 1 unpaid bill | Existing unpaid bill of ₹200 | previous_dues = 200 | _To be filled_ | ⬜ Pending |
| PREV-003 | Customer with multiple unpaid bills | 2 unpaid bills: ₹200, ₹150 | previous_dues = 350 | _To be filled_ | ⬜ Pending |
| PREV-004 | Paid bills don't count | 1 paid (₹200), 1 unpaid (₹150) | previous_dues = 150 | _To be filled_ | ⬜ Pending |

---

## 6. Integration Tests

### End-to-End Workflow Tests

| Test ID | Functionality | Test Steps | Expected Result | Actual Output | Status |
|---------|---------------|------------|-----------------|---------------|--------|
| INT-001 | Complete bill generation flow | 1. Register consumer<br/>2. Generate bill for 100 units<br/>3. Verify bill created | Bill with ₹200, due date set, status "Unpaid" | _To be filled_ | ⬜ Pending |
| INT-002 | Multiple bills for same customer | 1. Create bill 1 (100 units)<br/>2. Create bill 2 (50 units)<br/>3. Verify previous dues in bill 2 | Bill 2 has previous_dues = 200 | _To be filled_ | ⬜ Pending |
| INT-003 | Duplicate consumer number rejection | 1. Register consumer with 00000001<br/>2. Try to register another with 00000001 | Second registration rejected | _To be filled_ | ⬜ Pending |
| INT-004 | Name sanitization in registration | 1. Register "John123"<br/>2. Verify DB has "john" | Registration success, name sanitized | _To be filled_ | ⬜ Pending |
| INT-005 | Phone validation in registration | 1. Try to register with phone "12345"<br/>2. Verify error shown | Registration rejected with phone error | _To be filled_ | ⬜ Pending |

### Database Persistence Tests

| Test ID | Functionality | Test Steps | Expected Result | Actual Output | Status |
|---------|---------------|------------|-----------------|---------------|--------|
| DB-001 | Bill persists in database | 1. Create bill<br/>2. Query database<br/>3. Verify bill exists | Bill found with correct data | _To be filled_ | ⬜ Pending |
| DB-002 | Consumer persists with all fields | 1. Register consumer<br/>2. Query database<br/>3. Verify all fields | All fields (phone, consumer_number) present | _To be filled_ | ⬜ Pending |

---

## 7. User Interface Tests

### Web Form Tests

| Test ID | Functionality | Test Steps | Expected Result | Actual Output | Status |
|---------|---------------|------------|-----------------|---------------|--------|
| UI-001 | Household form shows validation errors | 1. Submit form with invalid name<br/>2. Check for error message | Error message displayed | _To be filled_ | ⬜ Pending |
| UI-002 | Consumer number auto-generated | 1. Leave consumer number blank<br/>2. Submit form | Consumer number generated (00000001, etc.) | _To be filled_ | ⬜ Pending |
| UI-003 | Bill displays all required fields | 1. Generate bill<br/>2. View bill page | Shows name, service#, date, units, dues, fine | _To be filled_ | ⬜ Pending |

---

## Test Execution Instructions

### Running Unit Tests

```bash
# Navigate to project directory
cd /home/coderzz69/Desktop/SE_Projects/electricity_billing_app

# Install pytest if not already installed
pip install pytest

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_validation.py -v
pytest tests/test_tariff.py -v

# Run with coverage report
pytest tests/ --cov=modules --cov=services --cov-report=html
```

### Manual Testing Procedure

1. **Start Application**:
   ```bash
   python app.py
   ```

2. **Test Consumer Registration**:
   - Navigate to http://localhost:5000
   - Login as admin (username: admin, password: admin123)
   - Try to add household with:
     - Invalid name: "John@Doe" → Should show error
     - Valid name with numbers: "John123" → Should succeed (sanitized to "john")
     - Invalid phone: "12345" → Should show error
     - Valid data → Should succeed and show consumer number

3. **Test Bill Generation**:
   - Select a household
   - Enter 0 units → Should show ₹25 minimum charge
   - Enter 100 units → Should show ₹200
   - Enter 150 units → Should show ₹375

4. **Test Previous Dues**:
   - Generate first bill for a household
   - Generate second bill → Should include previous bill in total

---

## Test Report Summary

| Category | Total Tests | Passed | Failed | Pending |
|----------|-------------|--------|--------|---------|
| Validation | 18 | 0 | 0 | 18 |
| Tariff Calculation | 11 | 0 | 0 | 11 |
| Bill Service | 6 | 0 | 0 | 6 |
| Fine Calculation | 3 | 0 | 0 | 3 |
| Previous Bills | 4 | 0 | 0 | 4 |
| Integration | 7 | 0 | 0 | 7 |
| UI Tests | 3 | 0 | 0 | 3 |
| **TOTAL** | **52** | **0** | **0** | **52** |

---

## Notes

- All test cases follow the Lab Task 2 requirements for test plan structure
- Test IDs are unique and descriptive
- Each test includes functionality description, input, expected output, and space for actual output
- Tests cover all major functionality: validation, calculation, bill creation, fine handling
- Integration tests verify end-to-end workflows
- Manual testing procedures provided for UI verification

**To update test results**: Run the tests and fill in the "Actual Output" and "Status" columns with:
- ✅ PASS - Test passed
- ❌ FAIL - Test failed
- ⬜ PENDING - Not yet executed
