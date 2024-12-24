#!/usr/bin/env python3
"""The module for Budget endpoints"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models.budget import Budget

budget_bp = Blueprint("budgets", __name__)


@budget_bp.route('/set', methods=['POST'], strict_slashes=False)
@jwt_required()
def set_budget():
    """Endpoint to set a budget"""
    data = request.json
    user_id = get_jwt_identity()
    month = data.get("month")
    limit_amount = data.get("limit_amount")

    if not month or not limit_amount:
        return jsonify({"error": "Month and limit_amount are required"}), 400

    existingBudget = Budget.query.filter_by(user_id=user_id,
                                            month=month).first()
    if existingBudget:
        existingBudget.limit_amount = amount
    else:
        newBudget = Budget(user_id=user_id, month=month,
                           limit_amount=limit_amount)
        db.session.add(newBudget)
    db.session.commit()
    return jsonify({"message": f'Budget for {month} set successfully'}), 201
