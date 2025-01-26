#!/usr/bin/env python3
"""The module for Summary of expenses and budgets endpoints"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from db import db
from models.budget import Budget
from models.transact import Transaction, TransactionType
from models.expense import Expense

summary_bp = Blueprint("summary", __name__)


@summary_bp.route('/get', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_summary():
    """Forms a summary report for the authenticated user."""
    try:
        user_id = int(get_jwt_identity())

        total_income = db.session.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.INCOME
        ).scalar()

        total_expenses = db.session.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.EXPENSE
        ).scalar()

        balance = total_income - total_expenses

        return jsonify({
            'totalIncome': total_income,
            'totalExpenses': total_expenses,
            'balance': balance
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database Error in Summary Route: {str(e)}")
        return jsonify({"error": "Database processing error"}), 500

    except Exception as e:
        print(f"Unexpected Error in Summary Route: {str(e)}")
        return jsonify({"error": "Unexpected error processing summary"}), 500
