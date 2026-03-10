from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi

app = Flask(__name__)
# Required for 'flash' messages to work
app.secret_key = "vanderbuild_admin_secure_key" 

ca = certifi.where()
uri = "mongodb+srv://Capstone:capstone@vbuild.ookltwu.mongodb.net/?appName=Vbuild"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=ca)
db = client["admins"]

EmployeeSalary_col = db["employeelogin"]      

new_employee = {
    "employee_id": "EMP002",
    "full_name": "Jedaiah Michael Yague",
    "password": "jed123", 
    "first_name": "Jedaiah Michael",
    "last_name": "Yague",
    "email": "McYageetz@gmail.com",
    "position": "Team Leader",
    "department": "Customer Support",
    "status": "Regular",
    "date_hired": "2024-05-05",
    "contract_expiry": "2027-06-03", 
    "Basic_Pay": 212000.00,
    "Regularization": "2024-06-05",
    "Sick_Leave": 13,
    "Vacation_Leave": 12,   
}


# 2. Use the correct method
try:
    result = EmployeeSalary_col.insert_one(new_employee)
    print(f"Successfully inserted with ID: {result.inserted_id}")
except Exception as e:
    print(f"An error occurred: {e}")

# 3. Verify
for x in EmployeeSalary_col.find():
    print(x)