#!/usr/bin/env python3
"""The module for Budget unittests"""
import unittest
from app import app, db
from flask_jwt_extended import create_access_token
from models.budget import Budget
from models.user import User


class TestBudgetRoutes(unittest.TestCase):
    """Unittesting for Budget"""
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
            tUser = User(
                id=1,
                email="test@example.com"
            )
            tUser.set_password("testpassword123")
            db.session.add(tUser)
            try:
                db.session.commit()
                print("Test user created successfully")
            except Exception as err:
                print(f'Error creating test user: {str(err)}')
                db.session.rollback()

    def tearDown(self):
        """Tear down test database."""
        with app.app_context():
            db.drop_all()
        self.app_context.pop()

    def testBudgetSet(self):
        """Testing budget is set correctly"""
        with app.app_context():
            token = create_access_token(identity='1')

        resp = self.app.post('/budgets/set', json={
            "month": "December",
            "limit_amount": 500
        }, headers={"Authorization": f'Bearer {token}'})

        self.assertEqual(resp.status_code, 201)
        self.assertIn("Budget for December set successfully",
                      resp.get_json().get("msg", ""))
