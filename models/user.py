#!/usr/bin/env python3
"""The module for User model"""
from db import db
from datetime import datetime


class User(db.Model):
    """A model named User for a database table named users"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(128), nullable=False)
