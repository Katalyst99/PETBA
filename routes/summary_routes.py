#!/usr/bin/env python3
"""The module for Summary of expenses and budgets endpoints"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models.budget import Budget
from models.expense import Expense

summary_bp = Blueprint("summary", __name__)


@summary_bp.route('/get', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_summary():
    """Forms a summary report for the authenticated user."""
    try:
        user_id = int(get_jwt_identity())
        month = request.args.get("month")

        if not month:
            print("Month parameter missing")
            return jsonify({"error": "Month parameter is required"}), 400

        budget = Budget.query.filter_by(user_id=user_id, month=month).first()

        if not budget:
            print(f'No budget found for month: {month}')
            return jsonify({"error": f'No budget set for {month}'}), 404

        expenses = Expense.query.filter_by(user_id=user_id, month=month).all()
        total = sum(exp.amount for exp in expenses)

        respData = {
            "month": month,
            "budget_limit": budget.limit_amount,
            "total_spent": total,
            "remaining_budget": budget.limit_amount - total
        }
        print(f'Sending response: {respData}')
        return jsonify(respData), 200

    except Exception as err:
        print(f'Error in get_summary: {str(err)}')
        return jsonify({"error": "Internal server error"}), 500
