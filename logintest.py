import os 
from dotenv import load_dotenv 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

load_dotenv() # To read database
app = Flask(__name__)
# babasahin ung ENV file para makuha database
app.secret_key = os.getenv("SECRET_KEY") 

# --- DATABASE CONNECTION ---
ca = certifi.where()
# same thing sa taas
uri = os.getenv("MONGO_URI") 
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=ca)
db = client["admins"]

admin_col = db["login"]      
employee_col = db["employeelogin"] 


# --- ROUTES 

@app.route('/')
def employee_home():
    return render_template('EmployeeLogin.html')

@app.route('/admin')
def admin_home():
    return render_template('AdminLogin.html')

@app.route('/login', methods=['POST'])
def login():
    user_type = request.form.get('user_type')
    entered_pass = request.form.get('password')

    if user_type == "admin":
        entered_user = request.form.get('email')
        user_record = admin_col.find_one({"username": entered_user})
    else:
        entered_user = request.form.get('employee_id')
        user_record = employee_col.find_one({"employee_id": entered_user})

    if user_record and user_record["password"] == entered_pass:
        session['user_id'] = str(user_record['_id'])
        session['role'] = user_type

        if user_type == "admin":
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('employee_dashboard'))

    flash("Invalid credentials.", "danger")
    return redirect(request.referrer)

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('admin_home'))
    
    emp_count = employee_col.count_documents({}) 
    return render_template('dashboard.html', count=emp_count)

@app.route('/employee-dashboard')
def employee_dashboard():
    if 'user_id' not in session or session.get('role') != 'employee':
        flash("Access Denied, Please Log in", "danger")
        return redirect(url_for('employee_home'))
    user_id = session.get('user_id')
    employee_data = employee_col.find_one({'_id': ObjectId(user_id)})
    return render_template('EmployeeDashboard.html',employee = employee_data )

@app.route('/logout')
def logout():
    session.clear() 
    flash("You have been logged out.", "info")
    return redirect(url_for('admin_home'))

@app.route('/mypayroll')
def mypayroll():
    # Fetch user data from database
    user_id = session.get('user_id')
    payroll_data = employee_col.find_one({'_id': ObjectId(user_id)})

    if payroll_data:
        # Get Basic Pay (Default to 0 if not found)
        basic_pay = payroll_data.get("Basic_Pay", 0)

        # Fixed Percentage Rates for payroll
        sss_rate = 0.045       # 4.5%
        philhealth_rate = 0.095 # 9.5%
        pagibig_rate = 0.045    # 4.5%

        # Perform Calculations
        sss_total = basic_pay * sss_rate
        phil_total = basic_pay * philhealth_rate
        pag_total = basic_pay * pagibig_rate

        total_deductions = sss_total + phil_total + pag_total
        after_tax = basic_pay - total_deductions

        # Send formatted strings to your HTML template
        return render_template('PayrollEmployee.html',
            basic_pay=f"{basic_pay:,.2f}",
            sss_val=f"{sss_total:,.2f}",
            phil_val=f"{phil_total:,.2f}",
            pag_val=f"{pag_total:,.2f}",
            total_deductions=f"{total_deductions:,.2f}",
            after_tax=f"{after_tax:,.2f}",
            employee=payroll_data
        )
    
    return "Payroll record not found.", 404

@app.route('/myprofile')
def myprofile():

    user_id = session.get('user_id')
    user_data = employee_col.find_one({'_id': ObjectId(user_id)})

    if user_data:

        return render_template('MyProfile.html', employee=user_data)

    return "User profile not found.", 404

@app.route('/leave_management')
def leave_management():
    selected_type = request.args.get('type', 'Vacation') 
    return render_template('leave_management.html', selected_type=selected_type)
  
if __name__ == '__main__':
    app.run(debug=True)