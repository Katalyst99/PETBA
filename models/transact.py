#!/usr/bin/env python3
"""The module for Transaction model"""
from db import db
from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Transaction(db.Model):
    """A model named Transaction for a database table named transactions"""
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Enum(TransactionType), nullable=False)
    description = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        print(f"Creating Transaction with kwargs: {kwargs}")  # Debug print
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<Transaction {self.id}: {self.type.value} {self.amount}>'
