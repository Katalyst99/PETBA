#!/usr/bin/env python3
"""The module for Transaction endpoints"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
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
        data = request.json
        user_id = int(get_jwt_identity())

        reqFlds = ['amount', 'category', 'type']
        if not all(field in data for field in reqFlds):
            return jsonify({"error": "Missing required fields"}), 400

        amount = data['amount']
        category = data['category']
        transType = data['type'].lower()

        if transType not in ['income', 'expense']:
            return jsonify({
                "error": "Invalid transaction type. Must be 'income' or 'expense'"
            }), 400

        transact = Transaction(
            user_id=user_id,
            amount=float(amount),
            category=category,
            type=TransactionType.INCOME if trans_type == 'income' else TransactionType.EXPENSE,
            description=data.get('description'),
            date=data.get('date')
        )
        db.session.add(transact)
        db.session.commit()

        return jsonify({
            "message": "Transaction added successfully",
            "transaction": {
                "id": transact.id,
                "amount": float(transact.amount),
                "category": transact.category,
                "type": transact.type.value,
                "date": transact.date.isoformat() if transaction.date else None,
                "description": transact.description
            }
        }), 201

    except Exception as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 500
