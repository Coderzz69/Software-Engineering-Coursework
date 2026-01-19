from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

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
    db = client.get_default_database()
    bills_collection = db['electricity_billing']
    households_collection = db['households']
    print(f"Connected to MongoDB database: {db.name}")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
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

    return redirect(url_for('index'))

@app.route('/add_household', methods=['POST'])
@login_required
def add_household():
    if households_collection is None:
        flash("Database connection error.", "error")
        return redirect(url_for('index'))
        
    try:
        household_name = request.form.get('household_name')
        house_number = request.form.get('house_number')
        
        # Check if exists (case insensitive)
        existing_household = households_collection.find_one({
            "house_number": {"$regex": f"^{house_number.strip()}$", "$options": "i"}
        })
        
        if existing_household:
            flash(f"Household with number {house_number} already exists.", "error")
        else:
            households_collection.insert_one({
                "household_name": household_name,
                "house_number": house_number,
                "created_at": datetime.now()
            })
            flash("Household added successfully!", "success")
    except Exception as e:
        flash(f"Error adding household: {e}", "error")
        
    return redirect(url_for('index'))

# Helper function for TSSPDCL Bill Calculation
def calculate_bill_amount(units):
    """
    Calculates the bill amount based on TSSPDCL Domestic Tariff (LT-I).
    Slabs (approximate for demo):
    0-50: 1.95
    51-100: 3.10
    101-200: 4.80
    201-400: 5.10
    401-800: 7.70
    >800: 9.00
    """
    total = 0
    remaining_units = units
    
    # Slab 1: 0-50
    if remaining_units > 0:
        slab_units = min(remaining_units, 50)
        total += slab_units * 1.95
        remaining_units -= slab_units
        
    # Slab 2: 51-100
    if remaining_units > 0:
        slab_units = min(remaining_units, 50)
        total += slab_units * 3.10
        remaining_units -= slab_units
        
    # Slab 3: 101-200
    if remaining_units > 0:
        slab_units = min(remaining_units, 100)
        total += slab_units * 4.80
        remaining_units -= slab_units
        
    # Slab 4: 201-400
    if remaining_units > 0:
        slab_units = min(remaining_units, 200)
        total += slab_units * 5.10
        remaining_units -= slab_units
        
    # Slab 5: 401-800
    if remaining_units > 0:
        slab_units = min(remaining_units, 400)
        total += slab_units * 7.70
        remaining_units -= slab_units
        
    # Slab 6: >800
    if remaining_units > 0:
        total += remaining_units * 9.00
        
    return round(total, 2)

@app.route('/add', methods=['POST'])
@login_required
def add_bill():
    if bills_collection is None:
        flash("Database connection error. Cannot add bill.", "error")
        return redirect(url_for('index'))

    try:
        household_id = request.form.get('household_id')
        units_consumed = float(request.form.get('units'))
        
        if units_consumed < 0:
            flash("Units must be a positive number.", "error")
            return redirect(url_for('index'))
        
        # Fetch household details
        household = households_collection.find_one({"_id": ObjectId(household_id)})
        if not household:
            flash("Selected household not found.", "error")
            return redirect(url_for('index'))
            
        total_amount = calculate_bill_amount(units_consumed)
        
        bill_data = {
            "household_id": ObjectId(household_id),
            "household_name": household.get('household_name'),
            "house_number": household.get('house_number'),
            "units": units_consumed,
            "rate": "TSSPDCL Tariff", # Placeholder or effective rate
            "total_amount": total_amount,
            "date": datetime.now()
        }
        
        bills_collection.insert_one(bill_data)
        flash(f"Bill added successfully! Amount: ₹{total_amount}", "success")
    except ValueError:
        flash("Invalid input. Please enter a number for units.", "error")
    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        
    return redirect(url_for('index'))

@app.route('/edit_bill/<bill_id>', methods=['GET', 'POST'])
@login_required
def edit_bill(bill_id):
    if bills_collection is None:
        flash("Database connection error.", "error")
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            household_id = request.form.get('household_id')
            units_consumed = float(request.form.get('units'))
            
            if units_consumed < 0:
                flash("Units must be a positive number.", "error")
                return redirect(url_for('edit_bill', bill_id=bill_id))
            
            # Fetch household details
            household = households_collection.find_one({"_id": ObjectId(household_id)})
            if not household:
                flash("Selected household not found.", "error")
                return redirect(url_for('edit_bill', bill_id=bill_id))
            
            total_amount = calculate_bill_amount(units_consumed)
            
            bills_collection.update_one(
                {'_id': ObjectId(bill_id)},
                {'$set': {
                    "household_id": ObjectId(household_id),
                    "household_name": household.get('household_name'),
                    "house_number": household.get('house_number'),
                    "units": units_consumed,
                    "rate": "TSSPDCL Tariff",
                    "total_amount": total_amount
                }}
            )
            flash(f"Bill updated successfully! New Amount: ₹{total_amount}", "success")
            return redirect(url_for('history'))
        except ValueError:
            flash("Invalid input.", "error")
        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            
    bill = bills_collection.find_one({'_id': ObjectId(bill_id)})
    
    # Fetch households for dropdown
    households = []
    if households_collection is not None:
        households = list(households_collection.find().sort("household_name", 1))
        
    return render_template('edit_bill.html', bill=bill, households=households)

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
