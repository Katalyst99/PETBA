#!/usr/bin/env python3
"""The module for Budget model"""
from db import db
from sqlalchemy import func
from datetime import datetime
from models.transact import Transaction, TransactionType


class Budget(db.Model):
    """A model named Budget for a database table named budgets"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    month = db.Column(db.String(10), nullable=False)
    limit_amount = db.Column(db.Float, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'month', name='unique_user_month'),
    )

    def calcSpent(self, session):
        """Calculate total expenses for this budget's month"""
        spent = session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == self.user_id,
            Transaction.type == TransactionType.EXPENSE,
            func.strftime('%Y-%m', Transaction.date) == self.month
        ).scalar() or 0
        return abs(spent)
