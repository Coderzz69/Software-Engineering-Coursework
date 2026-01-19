# ElectroBill - Electricity Billing App

A modern, Flask-based web application for managing household electricity bills, powered by MongoDB.

## Prerequisites

- Python 3.x
- MongoDB (Atlas or Local)

## Installation

1.  **Install Dependencies**:
    Initialize the environment and install dependencies using pipenv:
    ```bash
    pipenv install
    ```

2.  **Database Configuration (IMPORTANT)**:
    You need to connect the application to your MongoDB database. You have two options:

    **Option A: Using a .env file (Recommended)**
    1.  Create a file named `.env` in this directory (`/home/coderzz69/Desktop/SE_Projects/electricity_billing_app/`).
    2.  Add your connection string to it like this:
        ```text
        MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority
        ```
        *Replace `<username>`, `<password>`, `<cluster-url>`, and `<dbname>` with your actual MongoDB details.*

    **Option B: Hardcoding in `app.py`**
    1.  Open `app.py`.
    2.  Locate the "DATABASE CONFIGURATION" section (around line 15).
    3.  Uncomment the line `os.environ["MONGO_URI"] = ...` and paste your connection string there.

    *Note: If no URI is provided, the app will attempt to connect to a local MongoDB instance at `mongodb://localhost:27017/billing_db`.*

## Running the Application

1.  Start the Flask server using pipenv:
    ```bash
    pipenv run python app.py
    ```
    *Or activate the shell first with `pipenv shell` and then run `python app.py`.*

2.  Open your web browser and go to:
    `http://127.0.0.1:5000`

## Features

- **Dashboard**: View recent bills and add new readings.
- **Add Bill**: Calculate electricity costs based on units and rate.
- **History**: View a complete history of all billing records.
- **Modern UI**: Glassmorphism design with responsive layout.
