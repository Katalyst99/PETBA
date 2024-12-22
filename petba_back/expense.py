#!/usr/bin/env python3
"""The module for Expense model"""
from db import db
from datetime import datetime


class Expense(db.Model):
    """A model named Expense for a database table named expenses"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
