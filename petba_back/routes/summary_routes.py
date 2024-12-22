#!/usr/bin/env python3
"""The module for Summary of expenses and budgets endpoints"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from budget import Budget
from expense import Expense

summary_bp = Blueprint("summary", __name__)


@summary_bp.route('/summary', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_summary():
    """Forms a summary report for the authenticated user."""
    user_id = get_jwt_identity()
    month = request.args.get("month")

    if not month:
        return jsonify({"error": "Month parameter is required"}), 400

    budget = Budget.query.filter_by(user_id=user_id, month=month).first()
    if not budget:
        return jsonify({"error": f'No budget set for {month}'}), 404

    expenses = Expense.query.filter_by(user_id=user_id, month=month).all()
    total = sum(exp.amount for exp in expenses)

    return jsonify({
        "month": month,
        "budget_limit": budget.limit_amount,
        "total_spent": total_spent,
        "remaining_budget": budget.limit_amount - total
    }), 200
