#!/usr/bin/env python3
"""The module for Transaction endpoints"""
from datetime import datetime
from enum import Enum
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
        print(f"Transaction list error: {str(e)}")
        return jsonify({"error": str(err)}), 500


@transaction_bp.route('/add', methods=['POST'], strict_slashes=False)
@jwt_required()
def add_transaction():
    """Function to handle the POST /add route."""
    try:
        current_user_id = get_jwt_identity()
        print(f"Current User ID (JWT): {current_user_id}")
        print(f"JWT Identity Type: {type(current_user_id)}")

        data = request.json

        reqFlds = ['amount', 'category', 'type']
        for fld in reqFlds:
            if fld not in data:
                return jsonify({"error": f'Missing required field: {field}'}), 400

        transType = TransactionType(data['type'].lower())

        transaction = Transaction(
            user_id=int(current_user_id),
            amount=float(data['amount']),
            category=data['category'],
            type=transType,
            description=data.get('description', ''),
            date=datetime.strptime(data.get('date', datetime.utcnow().strftime('%Y-%m-%d')), '%Y-%m-%d')
        )

        db.session.add(transaction)
        db.session.commit()

        return jsonify({
            "message": "Transaction added successfully",
            "transaction": {
                "id": transaction.id,
                "amount": transaction.amount,
                "category": transaction.category,
                "type": transaction.type.value,
                "description": transaction.description,
                "date": transaction.date.isoformat()
            }
        }), 201

    except ValueError as err:
        return jsonify({"error": "Invalid transaction type"}), 400
    except Exception as e:
        db.session.rollback()
        print(f'Transaction Add Error: {e}')
        return jsonify({"error": str(e)}), 500
