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

Employeecol = db["employeelogin"]         

# --- DATA INSERTION WITH EXPIRY DATE ---

new_employee = {
    "employee_id": "EMP001",
    "full_name": "Daniel David A. Villarta",
    "password": "daniel112104", 
    "first_name": "Daniel David",
    "last_name": "Villarta",
    "email": "danielvillarta@gmail.com",
    "position": "Marketing Specialist",
    "department": "Marketing",
    "status": "Regular",
    "date_hired": "2024-03-05",
    "contract_expiry": "2027-03-05", 
    "Basic Pay": 17000.00,
    "Regularization": "2024-06-05",
    "Sick_Leave": 10,
    "Vacation_Leave": 12,   
}

try:
    Employeecol.update_one(
        {"employee_id": "EMP001"}, 
        {"$set": new_employee}, 
        upsert=True
    )
    print("Employee data updated with contract expiry.")
except Exception as e:
    print(f"Error: {e}")