# Virtual Shoe Store Ledger

This is a web application that provides a virtual ledger for a shoe store.

## Features

- A SQLite database to store data for sales, inventory, employees, payrolls, returns, coupons, and expenses.
- A web interface built with Flask to view and filter the data.
- A Generative AI-powered search and analysis page that allows users to query the database using natural language.
- Scripts to set up the database schema and populate it with synthetic data.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    - **sqlite3:** If you don't have sqlite3 installed, you can install it using your system's package manager.
      - On Debian/Ubuntu: `sudo apt-get install sqlite3`
    - **Python dependencies:** Install the required Python packages using pip.
      ```bash
      pip install -r requirements.txt
      ```

## Running the Application

1.  **Set up the database:**
    - Run the following scripts to create the database schema and populate it with three years of synthetic data.
      ```bash
      python database_setup.py
      python populate_database.py
      ```

2.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The application will be available at `http://127.0.0.1:5000`.
