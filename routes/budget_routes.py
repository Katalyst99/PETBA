#!/usr/bin/env python3
"""The module for Budget endpoints"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from db import db
from models.transact import Transaction, TransactionType
from models.budget import Budget

budget_bp = Blueprint("budgets", __name__)


@budget_bp.route('/list', methods=['GET'])
@jwt_required()
def list_budgets():
    """Function to handle the GET /list route."""
    try:
        user_id = int(get_jwt_identity())
        budgets = Budget.query.filter_by(user_id=user_id).all()

        budget_list = [{
            'month': budget.month,
            'limit': budget.limit_amount,
            'spent': budget.calculate_spent(db.session),
            'category': budget.month
        } for budget in budgets]

        return jsonify(budget_list), 200
    except Exception as e:
        print(f"Budget list error: {str(e)}")
        return jsonify({"error": "Failed to retrieve budgets"}), 500


@budget_bp.route('/set', methods=['POST'], strict_slashes=False)
@jwt_required()
def set_budget():
    """Endpoint to set a budget"""
    data = request.json
    user_id = int(get_jwt_identity())
    month = data.get("month")
    limit_amount = data.get("limit_amount")

    if not month or not limit_amount:
        return jsonify({"error": "Month and limit_amount are required"}), 400

    existingBudget = Budget.query.filter_by(user_id=user_id,
                                            month=month).first()
    if existingBudget:
        existingBudget.limit_amount = limit_amount
    else:
        newBudget = Budget(user_id=user_id, month=month,
                           limit_amount=limit_amount)
        db.session.add(newBudget)

    try:
        db.session.commit()
        return jsonify({"msg": f'Budget for {month} set successfully'}), 201
    except Exception as e:
        print("Database error:", str(e))
        db.session.rollback()
        return jsonify({"error": "Database error occurred"}), 500
