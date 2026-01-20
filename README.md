# ElectroBill - Electricity Billing App

A modern, Flask-based web application for managing household electricity bills, powered by MongoDB.

## Features

- **Dashboard**: View recent bills and add new readings.
- **Bill Calculation**: Automatically calculates electricity costs based on TSSPDCL Domestic Tariff (LT-I) slabs.
- **Household Management**: Add and manage households.
- **History & Search**: View a complete history of billing records and search by house number.
- **Admin Authentication**: Secure login for administrative tasks like adding/editing bills.
- **Modern UI**: Responsive layout with a glassmorphism design.

## Tech Stack

- **Backend**: Python, Flask
- **Database**: MongoDB
- **Frontend**: HTML, CSS, JavaScript

## Getting Started

### Prerequisites

- Python 3.x
- MongoDB (Atlas or Local)
- pip (or pipenv)

### Installation

1.  Navigate to the application directory:
    ```bash
    cd electricity_billing_app
    ```

2.  Install dependencies:

    Using pip:
    ```bash
    pip install -r requirements.txt
    ```

    Or using pipenv:
    ```bash
    pipenv install
    ```

3.  **Database Configuration**:
    Create a `.env` file in the `electricity_billing_app` directory with your MongoDB connection string. You can use the provided `.env.example` as a template or add the following:
    ```text
    MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority
    ```
    *If not provided, it defaults to `mongodb://localhost:27017/billing_db`.*

### Running the Application

1.  Start the server:
    ```bash
    python app.py
    ```
    (Or `pipenv run python app.py` if using pipenv)

2.  Open your browser and visit: `http://127.0.0.1:5000`

### Admin Login

- Default credentials (configurable via env vars `ADMIN_USERNAME` and `ADMIN_PASSWORD`):
  - Username: `admin`
  - Password: `admin123`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
