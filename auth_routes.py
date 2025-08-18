from flask import Blueprint, request, jsonify
from firebase_admin import auth
import mysql.connector
import re
from services.firebase_service import verify_firebase_token


auth_bp = Blueprint("auth", __name__)

# MySQL Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Kamra506#",
    database="outpass_db"
)
cursor = db.cursor()

# Email Validation (must be @ssn.edu.in)
def is_valid_ssn_email(email):
    return re.match(r"^[a-zA-Z0-9._%+-]+@ssn\.edu\.in$", email)

# Signup API
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")  # student, faculty, warden, security

    if not is_valid_ssn_email(email):
        return jsonify({"error": "Email must end with @ssn.edu.in"}), 400

    # Create user in Firebase
    try:
        user = auth.create_user(email=email, password=password, display_name=name)
        user_id = user.uid

        # Save user in MySQL
        cursor.execute(
            "INSERT INTO users (user_id, name, email, role) VALUES (%s, %s, %s, %s)",
            (user_id, name, email, role),
        )
        db.commit()

        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Login API (Firebase manages authentication)
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    token = data.get("token")

    if not token:
        return jsonify({"error": "Token required"}), 400

    decoded_user = verify_firebase_token(token)
    if not decoded_user:
        return jsonify({"error": "Invalid or expired token"}), 401

    return jsonify({"message": "Login successful", "user": decoded_user})
