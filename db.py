#!/usr/bin/env python3
"""DB module"""
from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
db = SQLAlchemy()


class Database:
    """The Db class"""
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv("SECRET_KEY")


try:
    engine = create_engine(Database.SQLALCHEMY_DATABASE_URI)
    engine.connect()
    print("Database connection successful.")
    engine.close()
except Exception as e:
    print(f'Database connection failed: {e}')


print(f"Loaded URI: {getenv('SQLALCHEMY_DATABASE_URI')}")
print(f"Loaded Secret Key: {getenv('SECRET_KEY')}")
