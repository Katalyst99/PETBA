#!/usr/bin/env python3
"""DB module"""
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Database:
    """The Db class"""
    SQLALCHEMY_DATABASE_URI = "sqlite:///petba.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your_secret_key_here"
