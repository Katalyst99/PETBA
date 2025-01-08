#!/usr/bin/env python3
"""The module for Budget model"""
from db import db
from datetime import datetime


class Budget(db.Model):
    """A model named Budget for a database table named budgets"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    month = db.Column(db.String(10), nullable=False)
    limit_amount = db.Column(db.Float, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'month', name='unique_user_month'),
    )
