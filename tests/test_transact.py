#!/usr/bin/env python3
"""The module for Transaction unittests"""
import unittest
from app import app, db
from flask_jwt_extended import create_access_token
from models.transact import Transaction


class TestTransactRoutes(unittest.TestCase):
    """Unittesting for Transactions"""
    def setUp(self):
        """Set up test variables."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['JWT_SECRET_KEY'] = 'Union'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down test database."""
        with app.app_context():
            db.drop_all()
        self.app_context.pop()

    def testTransactionAdd(self):
        """Testing transactions are added correctly"""
        with app.app_context():
            token = create_access_token(identity=1)
        resp = self.app.post('/transactions/add', json={
            "amount": 50,
            "category": "Food",
            "type": "Expense"
        }, headers={"Authorization": f'Bearer {token}'})
        self.assertEqual(resp.status_code, 201)
        self.assertIn("Transaction added successfully",
                      resp.get_json()["message"])
