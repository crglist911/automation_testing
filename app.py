from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('store.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sales')
def sales():
    conn = get_db_connection()
    query = """
        SELECT s.date, i.brand, i.name, s.quantity, s.total_price, s.customer_gender, s.customer_location
        FROM sales s
        JOIN inventory i ON s.inventory_id = i.id
    """
    filters = []
    params = []

    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    gender = request.args.get('gender')
    location = request.args.get('location')
    day_type = request.args.get('day_type')

    if year:
        filters.append("strftime('%Y', s.date) = ?")
        params.append(year)
    if month:
        filters.append("strftime('%m', s.date) = ?")
        params.append(month.zfill(2))
    if day:
        filters.append("strftime('%d', s.date) = ?")
        params.append(day.zfill(2))
    if gender:
        filters.append("s.customer_gender = ?")
        params.append(gender)
    if location:
        filters.append("s.customer_location = ?")
        params.append(location)
    if day_type:
        if day_type == 'weekday':
            filters.append("strftime('%w', s.date) NOT IN ('0', '6', '2')") # Exclude Sunday, Saturday, and Tuesday
        elif day_type == 'weekend':
            filters.append("strftime('%w', s.date) IN ('0', '6')")


    if filters:
        query += " WHERE " + " AND ".join(filters)

    sales_data = conn.execute(query, tuple(params)).fetchall()
    conn.close()
    return render_template('sales.html', sales=sales_data)


@app.route('/inventory')
def inventory():
    conn = get_db_connection()
    inventory_data = conn.execute('SELECT * FROM inventory').fetchall()
    conn.close()
    return render_template('inventory.html', inventory=inventory_data)


@app.route('/payrolls')
def payrolls():
    conn = get_db_connection()
    payrolls_data = conn.execute("""
        SELECT e.name, p.date, p.hours_worked, p.total_pay
        FROM payrolls p
        JOIN employees e ON p.employee_id = e.id
    """).fetchall()
    conn.close()
    return render_template('payrolls.html', payrolls=payrolls_data)


@app.route('/coupons')
def coupons():
    conn = get_db_connection()
    coupons_data = conn.execute('SELECT * FROM coupons').fetchall()
    conn.close()
    return render_template('coupons.html', coupons=coupons_data)


@app.route('/expenses')
def expenses():
    conn = get_db_connection()
    expenses_data = conn.execute('SELECT * FROM expenses').fetchall()
    conn.close()
    return render_template('expenses.html', expenses=expenses_data)


def parse_question_to_sql(question):
    question = question.lower()
    if "total sales in" in question:
        year = question.split("total sales in")[1].strip()
        return f"SELECT SUM(total_price) FROM sales WHERE strftime('%Y', date) = '{year}'", [f"Total Sales in {year}"]
    elif "how many shoes of" in question and "were sold" in question:
        brand = question.split("how many shoes of")[1].split("were sold")[0].strip()
        return f"SELECT SUM(s.quantity) FROM sales s JOIN inventory i ON s.inventory_id = i.id WHERE i.brand = '{brand.capitalize()}'", [f"Total {brand.capitalize()} Shoes Sold"]
    elif "total payroll in" in question:
        year = question.split("total payroll in")[1].strip()
        return f"SELECT SUM(total_pay) FROM payrolls WHERE strftime('%Y', date) = '{year}'", [f"Total Payroll in {year}"]
    elif "show me the inventory for" in question:
        brand = question.split("show me the inventory for")[1].strip()
        return f"SELECT brand, name, price, quantity FROM inventory WHERE brand = '{brand.capitalize()}'", ["Brand", "Name", "Price", "Quantity"]
    else:
        return None, None


@app.route('/ai_analysis', methods=['GET', 'POST'])
def ai_analysis():
    if request.method == 'POST':
        question = request.form['question']
        sql_query, headers = parse_question_to_sql(question)

        if sql_query:
            conn = get_db_connection()
            try:
                results = conn.execute(sql_query).fetchall()
                conn.close()
                return render_template('ai_analysis.html', question=question, results=results, headers=headers)
            except Exception as e:
                conn.close()
                return render_template('ai_analysis.html', question=question, error=str(e))
        else:
            return render_template('ai_analysis.html', question=question, error="I'm sorry, I don't understand that question.")

    return render_template('ai_analysis.html')


if __name__ == '__main__':
    app.run(debug=True)
