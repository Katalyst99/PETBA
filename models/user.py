#!/usr/bin/env python3
"""The module for User model"""
from db import db
from datetime import datetime
from flask_bcrypt import generate_password_hash


class User(db.Model):
    """A model named User for a database table named users"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def set_password(self, raw_password):
        """Method to correctly store hashed password"""
        self.password = generate_password_hash(raw_password).decode('utf-8')
