#!/usr/bin/env python3
"""The module for Authentication endpoints"""
from flask import Blueprint, request, jsonify
from flask_bcrypt import check_password_hash, Bcrypt
from flask_jwt_extended import create_access_token, JWTManager
from db import db
from models.user import User

bcrypt = Bcrypt()
jwt = JWTManager()
auth_bp = Blueprint("auth", __name__)


def create_jwt_token(user):
    return create_access_token(
        identity=str(user.id),  # Explicit string conversion
        additional_claims={
            'user_id': str(user.id)  # Redundant string conversion
        }
    )


@auth_bp.route('/register', methods=['POST'], strict_slashes=False)
def register():
    """Function to respond to the POST /register route."""
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    exists = User.query.filter_by(email=email).first()
    if exists:
        return jsonify({"error": "Email already registered"}), 400

    try:
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
    except ValueError as error:
        return jsonify({"error": f'Password hashing failed: {error}'}), 500

    user = User(email=email, password=hashed)
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=user.id)

    return jsonify({
        "message": "User registered successfully",
        "token": access_token,
        "user": {
            "id": user.id,
            "email": user.email
        }
    }), 201


@auth_bp.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """Function to respond to the POST /login route."""
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({
        "token": access_token,
        "user": {
            "id": user.id,
            "email": user.email
        }
    }), 200
