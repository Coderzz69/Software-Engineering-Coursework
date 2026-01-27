# ElectroBill 2.0 - Electricity Billing System
## Software Engineering Lab Tasks 1 & 2 Implementation

[![Tests](https://img.shields.io/badge/tests-36%20passed-brightgreen)]()
[![Documentation](https://img.shields.io/badge/docs-complete-blue)]()
[![Python](https://img.shields.io/badge/python-3.10-blue)]()

A comprehensive electricity billing system implementing Lab Tasks 1 & 2 requirements with modular architecture, comprehensive validation, and complete documentation.

---

## 🎯 Lab Tasks Implementation Status

### ✅ Task 1: Core Bill Generation System

- ✅ **Input Validation**
  - Names: Alphabets only (no numbers/special characters)
  - Phone: Exactly 10 digits
  - Service Number: Unique validation
  - Proper error handling with re-prompting

- ✅ **Bill Calculation** (Lab-Specified Rates)
  - First 50 units: ₹1.5 per unit
  - Next 50 units (51-100): ₹2.5 per unit
  - Next 50 units (101-150): ₹3.5 per unit
  - Above 150 units: ₹4.5 per unit
  - Minimum charge: ₹25 when units = 0

- ✅ **Output Display**
  - Consumer name, service number, date
  - Units consumed
  - Previous pending bills
  - Due date (payment within 15 days)
  - Amount after due date (with ₹150 fine)

- ✅ **Modular Programming**
  - Separate modules for input, validation, computation, and output
  - Reusable functions across application

### ✅ Task 2: Quality & Documentation

- ✅ **Modularization**
  - `modules/validation.py` - Input validation functions
  - `modules/input_handler.py` - User input collection
  - `modules/output_handler.py` - Bill formatting
  - `modules/constants.py` - Configuration constants
  - `services/tariff_service.py` - Bill calculation
  - `services/bill_service.py` - Bill management

- ✅ **Quality Characteristics**
  - **Usability**: Clear error messages, intuitive UI
  - **Efficiency**: Optimized database queries, O(1) calculations
  - **Reusability**: Modular functions, minimal dependencies
  - **Interoperability**: API endpoints for external access

- ✅ **Documentation**
  - `docs/MODULE_SPECIFICATIONS.md` - Complete module specs with algorithms
  - `docs/ALGORITHM_FLOWCHARTS.md` - Mermaid diagrams for workflows
  - `docs/TEST_PLAN.md` - 52 test cases with execution procedures

- ✅ **Test Plan**
  - 23 validation tests (100% pass rate)
  - 13 tariff calculation tests (100% pass rate)
  - Integration tests
  - Manual testing procedures

---

## 🏗️ Architecture

```
electricity_billing_app/
├── modules/              # Core business logic modules
│   ├── validation.py     # Input validation (names, phones, units)
│   ├── input_handler.py  # User input collection
│   ├── output_handler.py # Bill formatting & display
│   └── constants.py      # Configuration constants
├── services/             # Business services
│   ├── tariff_service.py # Bill calculation (lab rates)
│   └── bill_service.py   # Bill management
├── tests/                # Test suite
│   ├── test_validation.py
│   └── test_tariff.py
├── docs/                 # Documentation
│   ├── MODULE_SPECIFICATIONS.md
│   ├── ALGORITHM_FLOWCHARTS.md
│   └── TEST_PLAN.md
├── templates/            # Web UI templates
├── static/              # CSS/JS assets
└── app.py               # Flask application
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+
- MongoDB (local or Atlas)
- pip

### Installation Steps

1. **Navigate to project directory**:
   ```bash
   cd electricity_billing_app
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # or
   pipenv install
   ```

3. **Configure Database**:

   Create `.env` file in the `electricity_billing_app` directory:
   ```env
   MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=admin123
   ```
   *Note: If running locally, you might use `MONGO_URI=mongodb://localhost:27017/billing_db`*

4. **Run Application**:
   ```bash
   python3 app.py
   # or
   pipenv run python app.py
   ```

5. **Access Application**:
   - URL: http://localhost:5000
   - Admin Login: username=`admin`, password=`admin123`

---

## 🐳 Docker Support

To run the application using Docker:

1. **Navigate to project directory**:
   ```bash
   cd electricity_billing_app
   ```

2. **Run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

3. **Access Application**:
   - URL: http://localhost:5000
   - The database will be automatically provisioned in a container.

---

## 📋 Features

### 1. Consumer Management
- Register new consumers with validation
- Auto-generated service numbers (SVC00001, SVC00002, ...)
- Phone number validation (exactly 10 digits)
- Name validation (alphabets only)
- Duplicate service number prevention

### 2. Bill Generation
- Lab-specified tiered slab rates
- Minimum charge (₹25) for zero consumption
- Previous dues accumulation
- Automatic due date calculation (+15 days)
- Fine calculation (₹150 after due date)
- Detailed slab-wise breakdown

### 3. Bill Display
All required fields as per Lab Task 1:
- Consumer name and service number
- Bill date and due date
- Units consumed
- Current charges (slab-wise)
- Previous pending bills
- Total amount
- Amount after due date (with fine)

### 4. Search & History
- Search by service number
- View all bills
- Bill history per consumer
- Grand totals

---

## 🧪 Testing

Make sure you are in the `electricity_billing_app` directory.

### Run Unit Tests

```bash
# All tests
python3 -m pytest tests/ -v

# Validation tests only
python3 -m pytest tests/test_validation.py -v

# Tariff calculation tests only
python3 -m pytest tests/test_tariff.py -v

# With coverage report
python3 -m pytest tests/ --cov=modules --cov=services
```

### Test Results
```
tests/test_validation.py::23 tests ✅ PASSED (100%)
tests/test_tariff.py::13 tests ✅ PASSED (100%)
```

### Manual Testing

1. **Validation Testing**:
   - Try invalid name "John123" → Error shown
   - Try  invalid phone "12345" → Error shown
   - Try valid data → Success with service number

2. **Tariff Testing**:
   - 0 units → ₹25 (minimum charge)
   - 50 units → ₹75 (50 × 1.5)
   - 100 units → ₹200 (50×1.5 + 50×2.5)
   - 150 units → ₹375 (50×1.5 + 50×2.5 + 50×3.5)
   - 200 units → ₹600 (all slabs)

3. **Previous Dues Testing**:
   - Generate bill 1 (unpaid)
   - Generate bill 2 → Previous dues appear

---

## 📊 Tariff Rate Card

| Units Range | Rate per Unit | Example |
|-------------|---------------|---------|
| 0 | Minimum Charge | ₹25.00 |
| 1-50 | ₹1.5 | 50 units = ₹75 |
| 51-100 | ₹2.5 | 100 units = ₹200 |
| 101-150 | ₹3.5 | 150 units = ₹375 |
| 151+ | ₹4.5 | 200 units = ₹600 |

---

## 📚 Documentation

### Module Specifications
**Location**: `electricity_billing_app/docs/MODULE_SPECIFICATIONS.md`

Complete specifications for all modules including:
- Function name and purpose
- Input parameters with types
- Preconditions and postconditions
- Logic (algorithms in pseudocode)
- Output specifications
- Example usage

### Algorithm Flowcharts
**Location**: `electricity_billing_app/docs/ALGORITHM_FLOWCHARTS.md`

Mermaid diagrams for:
- Bill calculation algorithm
- Input validation workflow
- Complete bill generation process
- Previous dues calculation
- Fine calculation logic

### Test Plan
**Location**: `electricity_billing_app/docs/TEST_PLAN.md`

Comprehensive test plan with 52 test cases:
- 18 validation tests
- 11 tariff calculation tests
- 6 bill service tests
- 3 fine calculation tests
- 4 previous bills tests
- 7 integration tests
- 3 UI tests

---

## 🔧 API Endpoints (Interoperability)

### Consumer Management
```http
POST /add_household
- Registers new consumer with validation
- Auto-generates service number

GET /search?q=<service_number>
- Search bills by service number
```

### Bill Management
```http
POST /add
- Generate new bill
- Calculates previous dues automatically

GET /bill/<bill_id>
- View detailed bill invoice

GET /history
- View all bills
```

---

## 🎓 Lab Requirements Compliance

### Task 1 Requirements ✅

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Input validation (names) | ✅ | `validation.py::validate_consumer_name()` |
| Input validation (phone) | ✅ | `validation.py::validate_phone_number()` |
| Unique service number | ✅ | `validation.py::validate_service_number()` |
| Tariff rates (1.5/2.5/3.5/4.5) | ✅ | `tariff_service.py::calculate_bill()` |
| Minimum charge (₹25) | ✅ | `tariff_service.py` (zero units case) |
| Fine (₹150) | ✅ | `constants.py::FINE_AMOUNT` |
| Previous bills | ✅ | `bill_service.py::create_bill()` |
| Due date | ✅ | `bill_service.py` (+15 days) |
| Display all fields | ✅ | `output_handler.py::format_bill_display()` |
| Modular programming | ✅ | Separate modules for each function |

### Task 2 Requirements ✅

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| User-defined header files | ✅ | `modules/` directory with Python modules |
| Module specifications | ✅ | `docs/MODULE_SPECIFICATIONS.md` |
| Flowcharts | ✅ | `docs/ALGORITHM_FLOWCHARTS.md` |
| Test plan | ✅ | `docs/TEST_PLAN.md` |
| Usability | ✅ | Clear error messages, intuitive UI |
| Efficiency | ✅ | Optimized algorithms (O(1) tariff calc) |
| Reusability | ✅ | Modular, independent functions |
| Interoperability | ✅ | Web API endpoints |

---

## 👨‍💻 Development

### Adding New Validation Rules

```python
# Add to modules/validation.py
def validate_new_field(value):
    """
    Validate new field.

    Input: value (type)
    Output: (bool, str) - (is_valid, error_message)
    """
    if not condition:
        return False, "Error message"
    return True, ""
```

### Modifying Tariff Rates

```python
# Update modules/constants.py
TARIFF_SLABS = [
    (50, 1.5),  # Modify rates here
    (50, 2.5),
    # ...
]
```

---

##  License

Academic project for Software Engineering Lab coursework.

---

## 📞 Support

For issues or questions regarding the implementation:
- Review documentation in `electricity_billing_app/docs/` directory
- Check test files in `electricity_billing_app/tests/` for examples
- Review module specifications for API details
