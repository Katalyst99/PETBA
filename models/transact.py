#!/usr/bin/env python3
"""The module for Transaction model"""
from db import db
from datetime import datetime


class Transaction(db.Model):
    """A model named Transaction for a database table named transactions"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
