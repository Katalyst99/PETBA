#!/usr/bin/env python3
"""The module for Transaction endpoints"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from db import db
from models.transact import Transaction, TransactionType

transaction_bp = Blueprint("transactions", __name__)


@transaction_bp.route('/list', methods=['GET'], strict_slashes=False)
@jwt_required()
def list_transactions():
    """Function to handle the GET /list route."""
    try:
        user_id = int(get_jwt_identity())
        transacts = Transaction.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'id': trans.id,
            'amount': float(trans.amount),
            'category': trans.category,
            'type': trans.type.value,
            'date': trans.date.isoformat() if trans.date else None,
            'description': trans.description if hasattr(trans, 'description') else None
        } for trans in transacts]), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 500


@transaction_bp.route('/add', methods=['POST'], strict_slashes=False)
@jwt_required()
def add_transaction():
    """Function to handle the POST /add route."""
    try:
        # Comprehensive logging
        print("\n--- Transaction Add Endpoint ---")
        print("Headers:", dict(request.headers))
        print("Full Request Data:", request.get_data(as_text=True))
        print("Parsed JSON:", request.json)

        data = request.json
        print("Received data type:", type(data))

        user_id = int(get_jwt_identity())
        print("User ID:", user_id)

        # Validate required fields
        reqFlds = ['amount', 'category', 'type']
        if not all(field in data for field in reqFlds):
            missing = [f for f in reqFlds if f not in data]
            print(f"Missing fields: {missing}")
            return jsonify({"error": f"Missing required fields: {missing}"}), 400

        try:
            # Explicit type conversion and validation
            transaction_data = {
                'user_id': user_id,
                'amount': float(data['amount']),
                'category': str(data['category']),
                'type': TransactionType.INCOME if data['type'].lower() == 'income' else TransactionType.EXPENSE,
                'description': str(data.get('description', '')),
                'date': datetime.strptime(data['date'], '%Y-%m-%d') if data.get('date') else datetime.utcnow()
            }

            print("Processed transaction data:", transaction_data)

            transact = Transaction(**transaction_data)
            db.session.add(transact)
            db.session.commit()

            return jsonify({
                "message": "Transaction added successfully",
                "transaction": {
                    "id": transact.id,
                    "amount": float(transact.amount),
                    "category": transact.category,
                    "type": transact.type.value,
                    "date": transact.date.isoformat() if transact.date else None,
                    "description": transact.description
                }
            }), 201

        except ValueError as ve:
            print(f"Value Error: {ve}")
            return jsonify({"error": f"Data validation error: {str(ve)}"}), 400

    except Exception as err:
        db.session.rollback()
        print(f"Error in add_transaction: {str(err)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": str(err)}), 500
