from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from services.bill_service import BillService
import re

# Load environment variables if .env file exists
load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a random secret key for session security

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple User Class for Admin
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id == 'admin':
        return User('admin')
    return None

# ==================================================================================
# DATABASE CONFIGURATION
# ==================================================================================
mongo_uri = os.environ.get("MONGO_URI")

# Default to a local instance if no URI is provided
if not mongo_uri:
    print("WARNING: MONGO_URI not found. Using default local connection 'mongodb://localhost:27017/billing_db'")
    mongo_uri = "mongodb://localhost:27017/billing_db"

try:
    client = MongoClient(mongo_uri)
    db = client.get_default_database()
    
    # Initialize Collections
    households_collection = db['households']
    bills_collection = db['electricity_billing']
    
    # Initialize Services
    bill_service = BillService(db)
    
    print(f"Connected to MongoDB database: {db.name}")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    bill_service = None
    households_collection = None
    bills_collection = None

# ==================================================================================

@app.route('/')
def index():
    recent_bills = []
    if current_user.is_authenticated:
        # Admin View: Show recent bills
        if bills_collection is not None:
            recent_bills = list(bills_collection.find().sort("date", -1).limit(5))
        
        households = []
        if households_collection is not None:
            households = list(households_collection.find().sort("household_name", 1))
            
        return render_template('index.html', recent_bills=recent_bills, households=households)
    else:
        # Guest View: Show Search
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin_user = os.environ.get('ADMIN_USERNAME', 'admin')
        admin_pass = os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        if username == admin_user and password == admin_pass:
            user = User('admin')
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials.', 'error')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/add_household', methods=['POST'])
@login_required
def add_household():
    if households_collection is None:
        flash("Database connection error.", "error")
        return redirect(url_for('index'))
        
    try:
        # Import validation functions
        from modules.validation import validate_consumer_name, validate_phone_number, validate_consumer_number
        
        household_name = request.form.get('household_name', '').strip()
        # Sanitize name: remove numbers and convert to lowercase
        household_name = re.sub(r'\d+', '', household_name).lower()
        
        house_number = request.form.get('house_number', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        connection_type = request.form.get('connection_type', 'Household')
        
        # Generate or get consumer number
        consumer_number = request.form.get('service_number', '').strip()  # Form field name might still be service_number
        if not consumer_number:
            # Auto-generate consumer number
            last_household = households_collection.find_one(sort=[("created_at", -1)])
            if last_household and 'service_number' in last_household:
                # Extract number from last consumer number
                try:
                    last_num = int(last_household['service_number'])
                    new_num = last_num + 1
                except ValueError:
                    new_num = 1
            else:
                new_num = 1
            consumer_number = f"{new_num:08d}"  # Format: 00000001
        
        # Validate all inputs
        errors = []
        
        # Validate name
        name_valid, name_error = validate_consumer_name(household_name)
        if not name_valid:
            errors.append(name_error)
        
        # Validate phone
        phone_valid, phone_error = validate_phone_number(phone)
        if not phone_valid:
            errors.append(phone_error)
        
        # Validate consumer number (check uniqueness)
        consumer_valid, consumer_error = validate_consumer_number(consumer_number, households_collection)
        if not consumer_valid:
            errors.append(consumer_error)
        
        # If any validation errors, display them and return
        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for('index'))
        
        # Check if house number already exists (case insensitive)
        existing_household = households_collection.find_one({
            "house_number": {"$regex": f"^{house_number}$", "$options": "i"}
        })
        
        if existing_household:
            flash(f"Household with house number {house_number} already exists.", "error")
        else:
            # Insert new household with all fields
            households_collection.insert_one({
                "household_name": household_name,
                "service_number": consumer_number,  # Keep field name as service_number in DB
                "phone": phone,
                "house_number": house_number,
                "address": address,
                "connection_type": connection_type,
                "outstanding_balance": 0.0,
                "created_at": datetime.now()
            })
            flash(f"Household added successfully! Consumer Number: {consumer_number}", "success")
    except Exception as e:
        flash(f"Error adding household: {e}", "error")
        
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
@login_required
def add_bill():
    if bill_service is None:
        flash("Database connection error. Cannot add bill.", "error")
        return redirect(url_for('index'))

    try:
        household_id = request.form.get('household_id')
        units_consumed = float(request.form.get('units'))
        fine_amount = float(request.form.get('fine_amount', 0))
        
        if units_consumed < 0:
            flash("Units must be a positive number.", "error")
            return redirect(url_for('index'))
        
        bill_data = {
            "household_id": household_id,
            "units": units_consumed,
            "fine_amount": fine_amount
        }
        
        bill_service.create_bill(bill_data)
        flash(f"Bill generated successfully!", "success")
        
    except ValueError as ve:
        flash(f"Invalid input: {ve}", "error")
    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        
    return redirect(url_for('index'))

@app.route('/delete_bill/<bill_id>', methods=['POST'])
@login_required
def delete_bill(bill_id):
    if bills_collection is None:
        flash("Database connection error. Cannot delete bill.", "error")
        return redirect(url_for('history'))
        
    try:
        result = bills_collection.delete_one({'_id': ObjectId(bill_id)})
        if result.deleted_count > 0:
            flash("Bill deleted successfully.", "success")
        else:
            flash("Bill not found.", "error")
    except Exception as e:
        flash(f"Error deleting bill: {e}", "error")
        
    return redirect(url_for('history'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        house_number = request.form.get('house_number')
        return redirect(url_for('search', q=house_number))
        
    query = request.args.get('q')
    results = []
    
    if query and bills_collection is not None:
        results = list(bills_collection.find({"house_number": query}).sort("date", -1))
        
    grand_total = sum(bill.get('total_amount', 0) for bill in results)
        
    return render_template('history.html', bills=results, search_query=query, is_search=True, grand_total=grand_total)

@app.route('/history')
def history():
    all_bills = []
    if bills_collection is not None:
        all_bills = list(bills_collection.find().sort("date", -1))
        
    grand_total = sum(bill.get('total_amount', 0) for bill in all_bills)
    
    return render_template('history.html', bills=all_bills, is_search=False, grand_total=grand_total)

@app.route('/bill/<bill_id>')
def view_bill(bill_id):
    if bills_collection is None:
        flash("Database connection error.", "error")
        return redirect(url_for('history'))
        
    try:
        bill = bills_collection.find_one({'_id': ObjectId(bill_id)})
        if not bill:
            flash("Bill not found.", "error")
            return redirect(url_for('history'))
            
        return render_template('invoice.html', bill=bill)
    except Exception as e:
        flash(f"Error retrieving bill: {e}", "error")
        return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
