#!/usr/bin/env python3
"""The module for Transaction endpoints"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models.transact import Transaction

transaction_bp = Blueprint("transactions", __name__)


@transaction_bp.route('/add', methods=['POST'], strict_slashes=False)
@jwt_required()
def add_transaction():
    """Function to respond to the POST /add route."""
    data = request.json
    user_id = get_jwt_identity()
    amount = data.get("amount")
    category = data.get("category")
    trans_type = data.get("type")

    if not all([amount, category, trans_type]):
        return jsonify({"error": "All fields are required"}), 400

    transaction = Transaction(user_id=user_id, amount=amount,
                              category=category, type=trans_type)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction added successfully"}), 201
