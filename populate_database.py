import sqlite3
import random
from datetime import date, timedelta

def populate_database():
    conn = sqlite3.connect('store.db')
    c = conn.cursor()

    # Clear existing data
    for table in ['sales', 'inventory', 'employees', 'payrolls', 'returns', 'coupons', 'expenses']:
        c.execute(f"DELETE FROM {table}")

    # Populate employees
    employees = [('John Doe', 25.0), ('Jane Smith', 25.0), ('Peter Jones', 25.0)]
    c.executemany("INSERT INTO employees (name, hourly_rate) VALUES (?, ?)", employees)
    employee_ids = [row[0] for row in c.execute("SELECT id FROM employees")]

    # Populate inventory
    brands = ['Nike', 'Adidas', 'Puma', 'Reebok', 'New Balance', 'Asics', 'Converse', 'Vans']
    inventory = []
    total_inventory_value = 0
    while total_inventory_value < 200000:
        brand = random.choice(brands)
        name = f"{brand} Model {random.randint(1, 100)}"
        price = round(random.uniform(20.0, 2000.0), 2)
        quantity = random.randint(10, 50)
        inventory.append((brand, name, price, quantity))
        total_inventory_value += price * quantity
    c.executemany("INSERT INTO inventory (brand, name, price, quantity) VALUES (?, ?, ?, ?)", inventory)
    inventory_ids = [row[0] for row in c.execute("SELECT id FROM inventory")]

    # Populate sales, payrolls, returns, coupons, and expenses for the last 3 years
    start_date = date.today() - timedelta(days=3*365)
    end_date = date.today()
    current_date = start_date

    while current_date <= end_date:
        weekday = current_date.weekday()

        # Sales
        if weekday != 1:  # Not Tuesday
            if weekday < 5:  # Weekday
                num_sales = random.randint(50, 100)
            else:  # Weekend
                num_sales = random.randint(100, 200)

            for _ in range(num_sales):
                inventory_id = random.choice(inventory_ids)
                quantity = random.randint(1, 3)
                price = c.execute("SELECT price FROM inventory WHERE id = ?", (inventory_id,)).fetchone()[0]
                total_price = price * quantity
                customer_gender = 'Male' if random.random() < 0.6 else 'Female' # 60% male
                customer_location = 'Local' if random.random() < 0.9 else 'Out of State'
                c.execute("INSERT INTO sales (date, inventory_id, quantity, total_price, customer_gender, customer_location) VALUES (?, ?, ?, ?, ?, ?)",
                          (current_date, inventory_id, quantity, total_price, customer_gender, customer_location))

        # Payrolls
        if weekday != 1: # Not Tuesday
            if weekday < 5: # Weekday
                employees_on_duty = random.sample(employee_ids, 2)
            else: # Weekend
                employees_on_duty = employee_ids

            for employee_id in employees_on_duty:
                hours_worked = 8
                rate = c.execute("SELECT hourly_rate FROM employees WHERE id = ?", (employee_id,)).fetchone()[0]
                total_pay = hours_worked * rate
                c.execute("INSERT INTO payrolls (employee_id, date, hours_worked, total_pay) VALUES (?, ?, ?, ?)",
                          (employee_id, current_date, hours_worked, total_pay))

        # Monthly expenses and coupons
        if current_date.day == 1:
            # Rent
            c.execute("INSERT INTO expenses (date, name, amount) VALUES (?, ?, ?)", (current_date, 'Rent', 5000.0))
            # Electricity
            c.execute("INSERT INTO expenses (date, name, amount) VALUES (?, ?, ?)", (current_date, 'Electricity', random.uniform(500, 800)))
            # Coupons
            code = f"DISCOUNT{current_date.year}{current_date.month}"
            discount = round(random.uniform(0.05, 0.20), 2)
            c.execute("INSERT INTO coupons (code, discount_percentage, month, year) VALUES (?, ?, ?, ?)",
                      (code, discount, current_date.strftime("%B"), current_date.year))


        current_date += timedelta(days=1)


    # Returns (less than 5% of sales)
    sales_count = c.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
    num_returns = int(sales_count * random.uniform(0.01, 0.049))
    sales_ids = [row[0] for row in c.execute("SELECT id FROM sales ORDER BY RANDOM() LIMIT ?", (num_returns,))]
    for sale_id in sales_ids:
        return_date = c.execute("SELECT date FROM sales WHERE id = ?", (sale_id,)).fetchone()[0]
        return_date = date.fromisoformat(return_date) + timedelta(days=random.randint(1, 10))
        reason = random.choice(['Wrong size', 'Didn\'t like it', 'Defective'])
        c.execute("INSERT INTO returns (sale_id, date, reason) VALUES (?, ?, ?)", (sale_id, return_date, reason))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    populate_database()
    print("Database populated with synthetic data.")
