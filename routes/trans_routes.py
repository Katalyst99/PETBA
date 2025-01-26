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
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()

        reqFlds = ['amount', 'type', 'category', 'description', 'date']
        for fld in reqFlds:
            if fld not in data:
                return jsonify({
                    "status": "error",
                    "message": f'Missing required field: {fld}'
                }), 400

        transaction = Transaction(
            user_id=user_id,
            amount=data['amount'],
            type=TransactionType(data['type']),
            category=data['category'],
            description=data['description'],
            date=datetime.fromisoformat(data['date'])
        )
        db.session.add(transaction)
        db.session.commit()

        return jsonify({
            "status": 201,
            "data": {
                "message": "Transaction added successfully",
                "transaction": transaction.to_dict()
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
