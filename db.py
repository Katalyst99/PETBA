#!/usr/bin/env python3
"""DB module"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Database:
    """The Db class"""
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://petba_user:Katalyst@99@localhost/petba"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "your_secret_key_here"
