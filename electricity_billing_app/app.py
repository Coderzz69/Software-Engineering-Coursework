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
    bills_collection = db['electricity_billing']
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
        return render_template('index.html', recent_bills=recent_bills)
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

@app.route('/add', methods=['POST'])
@login_required
def add_bill():
    if bills_collection is None:
        flash("Database connection error. Cannot add bill.", "error")
        return redirect(url_for('index'))

    try:
        household_name = request.form.get('household_name')
        house_number = request.form.get('house_number')
        units_consumed = float(request.form.get('units'))
        rate_per_unit = float(request.form.get('rate', 0.12)) # Default rate
        
        total_amount = units_consumed * rate_per_unit
        
        bill_data = {
            "household_name": household_name,
            "house_number": house_number,
            "units": units_consumed,
            "rate": rate_per_unit,
            "total_amount": round(total_amount, 2),
            "date": datetime.now()
        }
        
        bills_collection.insert_one(bill_data)
        flash("Bill added successfully!", "success")
    except ValueError:
        flash("Invalid input. Please enter numbers for units and rate.", "error")
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
            household_name = request.form.get('household_name')
            house_number = request.form.get('house_number')
            units_consumed = float(request.form.get('units'))
            rate_per_unit = float(request.form.get('rate'))
            
            total_amount = units_consumed * rate_per_unit
            
            bills_collection.update_one(
                {'_id': ObjectId(bill_id)},
                {'$set': {
                    "household_name": household_name,
                    "house_number": house_number,
                    "units": units_consumed,
                    "rate": rate_per_unit,
                    "total_amount": round(total_amount, 2)
                }}
            )
            flash("Bill updated successfully!", "success")
            return redirect(url_for('history'))
        except ValueError:
            flash("Invalid input.", "error")
        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            
    bill = bills_collection.find_one({'_id': ObjectId(bill_id)})
    return render_template('edit_bill.html', bill=bill)

@app.route('/delete_bill/<bill_id>', methods=['POST'])
@login_required
def delete_bill(bill_id):
    if bills_collection is not None:
        try:
            bills_collection.delete_one({'_id': ObjectId(bill_id)})
            flash("Bill deleted successfully.", "success")
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
        
    return render_template('history.html', bills=results, search_query=query, is_search=True)

@app.route('/history')
def history():
    all_bills = []
    if bills_collection is not None:
        all_bills = list(bills_collection.find().sort("date", -1))
    return render_template('history.html', bills=all_bills, is_search=False)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
