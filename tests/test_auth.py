#!/usr/bin/env python3
"""The module for Authentication unittests"""
import unittest
from app import app, db
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from models.user import User

bcrypt = Bcrypt(app)


class TestAuthRoutes(unittest.TestCase):
    """Unittesting for Authentication"""
    def setUp(self):
        """Set up test variables."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://petba_user:Katalyst@99@localhost/test_db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_register(self):
        """Testing user registration"""
        resp = self.app.post('/auth/register', json={
            "email": "petba@example.com",
            "password": "password@12"
        })
        self.assertEqual(resp.status_code, 201)
        self.assertIn("User registered successfully",
                      resp.get_json().get("message", ""))

    def testValidLogin(self):
        """Testing for valid user login"""
        with app.app_context():
            hp = bcrypt.generate_password_hash('password@12').decode('utf-8')
            user = User(email="petba@example.com", password=hp)
            db.session.add(user)
            db.session.commit()

        resp = self.app.post('/auth/login', json={
            "email": "petba@example.com",
            "password": "password@12"
        })
        print("Response JSON:", resp.get_json())
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access_token', resp.get_json())

    def testInvalidLogin(self):
        """Testing for invalid user login"""
        resp = self.app.post('/auth/login', json={
            "email": "invalid@example.com",
            "password": "wrongpwd"
        })
        self.assertEqual(resp.status_code, 401)
        self.assertIn('Invalid credentials', resp.get_json().get("error", ""))
