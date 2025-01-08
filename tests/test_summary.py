#!/usr/bin/env python3
"""The module for Summary unittests"""
import unittest
from app import app, db
from flask_jwt_extended import create_access_token
from models.budget import Budget
from models.expense import Expense


class TestSummaryRoutes(unittest.TestCase):
    """Unittesting for Summaries"""
    def setUp(self):
        """Set up test variables."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            'mysql+mysqlconnector://petba_user:Katalyst@99@localhost/test_db'
        )
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

    def testSummaryGet(self):
        """Testing summaries are retrieved correctly"""
        with app.app_context():
            token = create_access_token(identity=1)
            budget = Budget(user_id=1, month="December", limit_amount=500)
            expense = Expense(user_id=1, category="Food", amount=50,
                              month="December")
            db.session.add(budget)
            db.session.add(expense)
            db.session.commit()

        resp = self.app.get('/summary/get?month=December',
                            headers={"Authorization": f'Bearer {token}'})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["month"], "December")
        self.assertEqual(data["budget_limit"], 500)
        self.assertEqual(data["total_spent"], 50)
        self.assertEqual(data["remaining_budget"], 450)
