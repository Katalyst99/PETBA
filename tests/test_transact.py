#!/usr/bin/env python3
"""The module for Transaction unittests"""
import unittest
from app import app, db
from flask_jwt_extended import create_access_token
from models.transact import Transaction, TransactionType
from models.user import User


class TestTransactRoutes(unittest.TestCase):
    """Unittesting for Transactions"""
    def setUp(self):
        """Set up test variables."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            'mysql+mysqlconnector://petba_user:Katalyst@99@localhost/test_db'
        )
        app.config['JWT_SECRET_KEY'] = 'Union'
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
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

    def testTransactionAdd(self):
        """Testing transactions are added correctly"""
        try:
            with app.app_context():
                tUser = User(email="test@example.com")
                tUser.set_password("testpassword123")
                db.session.add(tUser)
                db.session.commit()
                print(f'Created test user with ID: {tUser.id}')

                token = create_access_token(identity=str(tUser.id))
                print(f'Generated Token: {token}')

                resp = self.app.post('/transactions/add', json={
                    "amount": 50.0,
                    "category": "Food",
                    "type": "Expense"
                }, headers={"Authorization": f'Bearer {token}'})

                print(f'Response Status Code: {resp.status_code}')
                print(f'Response Data: {resp.get_data(as_text=True)}')

                self.assertEqual(resp.status_code, 201)
                self.assertIn("Transaction added successfully",
                              resp.get_json()["message"])

                trans = Transaction.query.filter_by(
                    user_id=tUser.id
                ).first()
                if trans is None:
                    print("Warning: No transaction found in database")
                else:
                    print(f"Found transaction: {trans.amount}, {trans.category}, {trans.type}")
                self.assertIsNotNone(trans)
                self.assertEqual(trans.amount, 50.0)
                self.assertEqual(trans.category, "Food")
                self.assertEqual(trans.type, TransactionType.EXPENSE)

        except Exception as err:
            print(f'Error in testTransactionAdd: {str(err)}')
            raise

    def testTransactionAddIncome(self):
        """Testing income transactions are added correctly"""
        with app.app_context():
            tUser = User(email="test2@example.com")
            tUser.set_password("testpassword123")
            db.session.add(tUser)
            db.session.commit()

            token = create_access_token(identity=str(tUser.id))
            incomeData = {
                "amount": 1000.0,
                "category": "Salary",
                "type": "income"
            }

            resp = self.app.post(
                '/transactions/add',
                json=incomeData,
                headers={"Authorization": f'Bearer {token}'}
            )

            self.assertEqual(resp.status_code, 201)
            trans = Transaction.query.filter_by(
                user_id=tUser.id
            ).first()
            self.assertEqual(trans.type, TransactionType.INCOME)

    def testTransactionFieldsMissing(self):
        """Testing transaction creation with missing fields"""
        with app.app_context():
            tUser = User(email="test3@example.com")
            tUser.set_password("testpassword123")
            db.session.add(tUser)
            db.session.commit()

            token = create_access_token(identity=str(tUser.id))
            resp = self.app.post(
                '/transactions/add',
                json={"category": "Food", "type": "expense"},
                headers={"Authorization": f'Bearer {token}'}
            )
            self.assertEqual(resp.status_code, 400)

            resp = self.app.post(
                '/transactions/add',
                json={"amount": 50.0, "type": "expense"},
                headers={"Authorization": f'Bearer {token}'}
            )
            self.assertEqual(resp.status_code, 400)

            resp = self.app.post(
                '/transactions/add',
                json={"amount": 50.0, "category": "Food"},
                headers={"Authorization": f'Bearer {token}'}
            )
            self.assertEqual(resp.status_code, 400)

    def testTransactionInvalidType(self):
        """Testing transaction creation with invalid type"""
        with app.app_context():
            tUser = User(email="test4@example.com")
            tUser.set_password("testpassword123")
            db.session.add(tUser)
            db.session.commit()

            token = create_access_token(identity=str(tUser.id))
            resp = self.app.post(
                '/transactions/add',
                json={
                    "amount": 50.0,
                    "category": "Food",
                    "type": "invalid_type"
                },
                headers={"Authorization": f'Bearer {token}'}
            )
            self.assertEqual(resp.status_code, 400)

    def testTransactionNoAuth(self):
        """Testing transaction creation without user authentication"""
        resp = self.app.post(
            '/transactions/add',
            json={
                "amount": 50.0,
                "category": "Food",
                "type": "expense"
            }
        )
        self.assertEqual(resp.status_code, 401)


if __name__ == '__main__':
    unittest.main(verbosity=2)
