#!/usr/bin/env python3
"""The module for Transaction endpoints"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models.transact import Transaction, TransactionType

transaction_bp = Blueprint("transactions", __name__)


@transaction_bp.route('/list', methods=['GET'], strict_slashes=False)
@jwt_required()
def lisTransaction():
    """Function to handle the GET /list route."""
    try:
        data = request.json
        user_id = int(get_jwt_identity())
        trans = Transaction.query.filter_by(user_id=user_id).all()
        amount = data.get("amount")
        category = data.get("category")
        transType = data.get("type")

        if not all([amount, category, transType]):
            return jsonify({"error": "All fields are required"}), 400

        try:
            if transType.lower() == "income":
                transType = TransactionType.INCOME
            elif transType.lower() == "expense":
                transType = TransactionType.EXPENSE
            else:
                return jsonify({
                    "error": "Invalid transaction type. Must be 'income' or 'expense'"
                }), 400
        except AttributeError:
            return jsonify({
                "error": "Invalid transaction type format"
            }), 400

        trans = Transaction(user_id=user_id, amount=float(amount),
                            category=category, type=transType)
        db.session.add(trans)
        db.session.commit()

        return jsonify({"message": "Transaction added successfully"}), 201

    except Exception as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 500
