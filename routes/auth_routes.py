#!/usr/bin/env python3
"""The module for Authentication endpoints"""
from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, JWTManager
from db import db
from models.user import User

bcrypt = Bcrypt()
jwt = JWTManager()
auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/register', methods=['POST'], strict_slashes=False)
def register():
    """Function to respond to the POST /register route."""
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """Function to respond to the POST /login route."""
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access_token": access_token}), 200

    return jsonify({"error": "Invalid credentials"}), 401
