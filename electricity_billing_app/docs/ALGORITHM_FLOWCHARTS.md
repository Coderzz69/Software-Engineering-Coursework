# Algorithm Flowcharts
## Electricity Billing System - Lab Tasks 1 & 2

**Author**: Software Engineering Lab  
**Date**: 2026-01-27

This document contains flowcharts for key algorithms in the electricity billing system, created using Mermaid diagram syntax.

---

## 1. Bill Calculation Algorithm

This flowchart shows the tiered slab-based bill calculation as per Lab Task 1 specifications.

```mermaid
flowchart TD
    Start([Start: Calculate Bill]) --> Input[/"Input: units_consumed"/]
    Input --> CheckZero{units == 0?}
    
    CheckZero -->|Yes| MinCharge[Apply minimum charge: ₹25]
    CheckZero -->|No| InitVars[Initialize:<br/>total = 0<br/>remaining = units<br/>breakdown = []]
    
    InitVars --> Slab1{remaining > 0?}
    
    Slab1 -->|Yes| Calc1["Calculate Slab 1-50:<br/>slab_units = min(remaining, 50)<br/>amount = slab_units × 1.5"]
    Calc1 --> Update1["Update:<br/>total += amount<br/>remaining -= slab_units<br/>breakdown.append(...)"]
    Slab1 -->|No| Done
    
    Update1 --> Slab2{remaining > 0?}
    
    Slab2 -->|Yes| Calc2["Calculate Slab 51-100:<br/>slab_units = min(remaining, 50)<br/>amount = slab_units × 2.5"]
    Calc2 --> Update2["Update:<br/>total += amount<br/>remaining -= slab_units<br/>breakdown.append(...)"]
    Slab2 -->|No| Done
    
    Update2 --> Slab3{remaining > 0?}
    
    Slab3 -->|Yes| Calc3["Calculate Slab 101-150:<br/>slab_units = min(remaining, 50)<br/>amount = slab_units × 3.5"]
    Calc3 --> Update3["Update:<br/>total += amount<br/>remaining -= slab_units<br/>breakdown.append(...)"]
    Slab3 -->|No| Done
    
    Update3 --> Slab4{remaining > 0?}
    
    Slab4 -->|Yes| Calc4["Calculate Slab 151+:<br/>slab_units = remaining<br/>amount = slab_units × 4.5"]
    Calc4 --> Update4["Update:<br/>total += amount<br/>breakdown.append(...)"]
    Slab4 -->|No| Done
    
    Update4 --> Done
    MinCharge --> Done
    Done([Return: total, breakdown])
```

### Example Calculation Flow

Consider 175 units consumed:

1. **Slab 1 (1-50)**: 50 × 1.5 = ₹75, remaining = 125
2. **Slab 2 (51-100)**: 50 × 2.5 = ₹125, remaining = 75
3. **Slab 3 (101-150)**: 50 × 3.5 = ₹175, remaining = 25
4. **Slab 4 (151+)**: 25 × 4.5 = ₹112.5, remaining = 0
5. **Total**: ₹487.50

---

## 2. Input Validation Flowchart

This flowchart shows the validation process for consumer registration.

```mermaid
flowchart TD
    Start([Start: Validate Consumer Data]) --> GetName[/"Input: name, phone, consumer_number"/]
    
    GetName --> SanitizeName["Sanitize Name:<br/>Lowercase & Remove Numbers"]
    SanitizeName --> ValName{Validate Name:<br/>Alphabets only?}
    ValName -->|Invalid| ErrName["Error:<br/>'Name must contain only alphabets'"]
    ValName -->|Valid| ValPhone{Validate Phone:<br/>Exactly 10 digits?}
    
    ValPhone -->|Invalid| ErrPhone["Error:<br/>'Phone must be exactly 10 digits'"]
    ValPhone -->|Valid| ValService{Validate Consumer Number:<br/>Numeric & Unique?}
    
    ValService -->|Invalid| ErrService["Error:<br/>'Invalid or Duplicate Consumer Number'"]
    ValService -->|Valid| Success["All validations passed"]
    
    ErrName --> CollectErrors[Collect all errors]
    ErrPhone --> CollectErrors
    ErrService --> CollectErrors
    
    CollectErrors --> DisplayErrors["Display errors to user"]
    DisplayErrors --> Reprompt["Re-prompt for input"]
    Reprompt --> GetName
    
    Success --> Done([Return: Valid Data])
```

---

## 3. Complete Bill Generation Process

This is the overall bill generation workflow from consumer registration to bill display.

```mermaid
flowchart TD
    Start([Start: Bill Generation]) --> CheckConsumer{Consumer<br/>exists?}
    
    CheckConsumer -->|No| RegStart["Start Consumer Registration"]
    RegStart --> InputDetails["Collect:<br/>- Name<br/>- Phone<br/>- Consumer Number<br/>- Address"]
    InputDetails --> Validate["Validate all inputs"]
    Validate --> ValResult{Valid?}
    ValResult -->|No| ShowErrors["Display errors"]
    ShowErrors --> InputDetails
    ValResult -->|Yes| SaveConsumer["Save consumer to database"]
    SaveConsumer --> GenServiceNum["Generate/Assign<br/>Consumer Number"]
    
    CheckConsumer -->|Yes| GetUnits
    GenServiceNum --> GetUnits["Input: Units consumed"]
    
    GetUnits --> ValUnits{Units >= 0?}
    ValUnits -->|No| ErrUnits["Error: Units cannot be negative"]
    ErrUnits --> GetUnits
    ValUnits -->|Yes| CalcBill["Calculate bill using<br/>TariffService"]
    
    CalcBill --> GetPrevDues["Query previous unpaid bills"]
    GetPrevDues --> CalcTotal["Calculate:<br/>Total = Current + Previous Dues + Fine"]
    CalcTotal --> SetDueDate["Set due date = Today + 15 days"]
    SetDueDate --> CreateBill["Create bill document"]
    CreateBill --> SaveBill["Save bill to database"]
    SaveBill --> FormatOutput["Format bill for display"]
    FormatOutput --> DisplayBill["Display bill to user"]
    DisplayBill --> Done([End])
```

---

## 4. Name Validation Detailed Flow

```mermaid
flowchart TD
    Start([Input: name]) --> CheckNull{name is<br/>null/empty?}
    CheckNull -->|Yes| ReturnErr1["Return:<br/>(False, 'Name cannot be empty')"]
    CheckNull -->|No| Trim["name = trim(name)"]
    Trim --> CheckPattern{"Matches pattern<br/>^[A-Za-z\s]+$ ?"}
    CheckPattern -->|No| ReturnErr2["Return:<br/>(False, 'Name must contain only alphabets')"]
    CheckPattern -->|Yes| ReturnOK["Return:<br/>(True, '')"]
    
    ReturnErr1 --> End([End])
    ReturnErr2 --> End
    ReturnOK --> End
```

---

## 5. Phone Number Validation Flow

```mermaid
flowchart TD
    Start([Input: phone]) --> CheckEmpty{phone is<br/>empty?}
    CheckEmpty -->|Yes| ReturnErr1["Return:<br/>(False, 'Phone number required')"]
    CheckEmpty -->|No| Trim["phone = trim(phone)"]
    Trim --> CheckLen{length == 10?}
    CheckLen -->|No| ReturnErr2["Return:<br/>(False, 'Phone must be exactly 10 digits')"]
    CheckLen -->|Yes| CheckDigits{"All digits?<br/>(matches ^\d{10}$)"}
    CheckDigits -->|No| ReturnErr3["Return:<br/>(False, 'Phone must contain only digits')"]
    CheckDigits -->|Yes| ReturnOK["Return:<br/>(True, '')"]
    
    ReturnErr1 --> End([End])
    ReturnErr2 --> End
    ReturnErr3 --> End
    ReturnOK --> End
```

---

## 6. Previous Dues Calculation Flow

```mermaid
flowchart TD
    Start([Input: household_id]) --> Query["Query database:<br/>Find all unpaid bills<br/>for household_id"]
    Query --> CheckResults{Bills<br/>found?}
    CheckResults -->|No| NoDues["previous_dues = 0"]
    CheckResults -->|Yes| InitSum["previous_dues = 0"]
    InitSum --> Loop["For each unpaid bill:"]
    Loop --> AddAmount["previous_dues += bill.total_amount"]
    AddAmount --> MoreBills{More<br/>bills?}
    MoreBills -->|Yes| Loop
    MoreBills -->|No| Return
    NoDues --> Return([Return: previous_dues])
    Return --> End([End])
```

---

## 7. Due Date & Fine Calculation

```mermaid
flowchart TD
    Start([Input: bill]) --> GetBillDate["bill_date = bill.date"]
    GetBillDate --> CalcDue["due_date = bill_date + 15 days"]
    CalcDue --> GetToday["today = current_date()"]
    GetToday --> Compare{today ><br/>due_date?}
    Compare -->|today <= due_date| NoFine["fine = 0<br/>amount = total"]
    Compare -->|today > due_date| ApplyFine["fine = 150<br/>amount = total + 150"]
    NoFine --> Done([Return: amount, fine])
    ApplyFine --> Done
```

---

## 8. Payment Gateway Process

```mermaid
flowchart TD
    Start([User Clicks 'Pay Now']) --> RenderPage["Render Payment Page<br/>(payment.html)"]
    RenderPage --> InputDetails[/"Input: Card Details"/]
    InputDetails --> Submit["Submit Payment"]
    
    Submit --> Process{Process<br/>Payment}
    Process -->|Success| UpdateDB["Update Bill Status:<br/>'Paid'"]
    UpdateDB --> RecordDate["Record Payment Date"]
    RecordDate --> Redirect["Redirect to Invoice"]
    Redirect --> ShowSuccess["Show 'Payment Successful'<br/>Message"]
    
    Process -->|Failure| ShowError["Show Error Message"]
    ShowError --> RenderPage
    
    ShowSuccess --> End([End])
```

---

## Summary of Algorithms

| Algorithm | Complexity | Key Operations |
|-----------|------------|----------------|
| Bill Calculation | O(1) | Fixed 4 slabs, constant time |
| Name Validation | O(n) | Regex match on name length (after sanitization) |
| Phone Validation | O(1) | Length and digit check |
| Consumer Number Check | O(1) | Database index lookup |
| Previous Dues | O(m) | m = number of unpaid bills |
| Bill Generation | O(1) | Constant operations |

All algorithms are optimized for efficiency with minimal database queries and linear/constant time complexity.
