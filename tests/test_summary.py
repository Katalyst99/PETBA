#!/usr/bin/env python3
"""The module for Summary unittests"""
import unittest
from os import getenv
from dotenv import load_dotenv
from app import app, db
from flask_jwt_extended import create_access_token
from models.budget import Budget
from models.expense import Expense
from models.user import User

load_dotenv()


class TestSummaryRoutes(unittest.TestCase):
    """Unittesting for Summaries"""
    def setUp(self):
        """Set up test variables."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = getenv('TEST_DATABASE_URI')
        app.config['SECRET_KEY'] = getenv('SECRET_KEY')
        app.config['JWT_SECRET_KEY'] = getenv('SECRET_KEY')
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        with app.app_context():
            db.drop_all()
            db.create_all()
            print("Test database initialized")

    def tearDown(self):
        """Tear down test database."""
        with app.app_context():
            db.session.remove()
            db.drop_all()
            print("Test database cleaned up")
        self.app_context.pop()

    def testSummaryGet(self):
        """Testing summaries are retrieved correctly"""
        with app.app_context():
            tUser = User(email="test@example.com")
            tUser.set_password("testpassword123")
            db.session.add(tUser)
            db.session.flush()
            print(f'Created test user with ID: {tUser.id}')

            tBudget = Budget(
                user_id=tUser.id,
                month="December",
                limit_amount=500.0
            )
            db.session.add(tBudget)

            tExpense = Expense(
                user_id=tUser.id,
                category="Food",
                amount=50.0,
                month="December"
            )
            db.session.add(tExpense)
            db.session.commit()

            token = create_access_token(identity=str(tUser.id))
            print(f'Generated Token: {token}')

            headers = {
                "Authorization": f'Bearer {token}',
                "Content-Type": "application/json"
            }

            resp = self.app.get(
                '/summary/get?month=December',
                headers=headers
            )

            self.assertEqual(resp.status_code, 200,
                             f'Expected 200 OK, got {resp.status_code}')

            if resp.status_code == 200:
                data = resp.get_json()
                self.assertEqual(data["month"], "December")
                self.assertEqual(data["budget_limit"], 500)
                self.assertEqual(data["total_spent"], 50)
                self.assertEqual(data["remaining_budget"], 450)


if __name__ == '__main__':
    unittest.main(verbosity=2)
